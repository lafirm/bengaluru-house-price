from flask import Flask,request,jsonify, render_template
import pickle
import json
import numpy as np

app = Flask(__name__)

with open('./artifacts/columns.json', 'r') as f:
    data_columns = json.load(f)['data_columns']
    locations = data_columns[3:]
with open('./artifacts/bengaluru_home_prices_model.pickle', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return render_template('app.html')

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    data = [str(x) for x in request.form.values()]
    total_sqft = float(data[0])
    bhk = int(data[1])
    bath = int(data[2])
    location = str(data[3])

    try:
        loc_index = data_columns.index(location.lower())
    except:
        loc_index = -1
    if loc_index==-1:
        return render_template("app.html", predicted_price="Not Available",
                               prediction_text="Please enter a valid location in Bengaluru!")
    x = np.zeros(len(data_columns))
    x[0] = total_sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1
    result =  round(model.predict([x])[0], 2)
    return render_template("app.html",predicted_price="{} Lakhs".format(result),
                           prediction_text='''A {}BHK house of {}sq.ft. with {} bathroom(s) in {}, Bengaluru costs {}
                                           Lakhs'''.format(bhk, int(total_sqft), bath, location.title(), result))

if __name__ == '__main__':
    print("Starting Python Flask Server for BLR Home Price Prediction")
    app.run(debug=True)