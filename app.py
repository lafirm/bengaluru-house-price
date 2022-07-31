from flask import Flask,request,jsonify, render_template
import pickle
import json
import numpy as np

app = Flask(__name__)

__locations = None
__data_columns = None
__model = None

@app.route('/')
def home():
    return render_template('app.html')

def load_saved_artifacts():
    print('Loading Saved Artifacts...')
    global __data_columns
    global __locations
    global __model
    with open('./artifacts/columns.json', 'r') as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]
    with open('./artifacts/bengaluru_home_prices_model.pickle', 'rb') as f:
        __model =  pickle.load(f)
    print("Artifacts were loaded successfully!")


@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': __locations
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    data = [str(x) for x in request.form.values()]
    total_sqft = float(data[0])
    bhk = int(data[1])
    bath = int(data[2])
    location = str(data[3])

    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1
    if loc_index==-1:
        return render_template("app.html", predicted_price="Not Available",
                               prediction_text="Please enter a valid location in Bengaluru!")
    x = np.zeros(len(__data_columns))
    x[0] = total_sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1
    result =  round(__model.predict([x])[0], 2)
    return render_template("app.html",predicted_price="{} Lakhs".format(result),
                           prediction_text='''A {}BHK house of {}sq.ft. with {} bathroom(s) in {}, Bengaluru costs {}
                                           Lakhs'''.format(bhk, int(total_sqft), bath, location.title(), result))

if __name__ == '__main__':
    print("Starting Python Flask Server for BLR Home Price Prediction")
    load_saved_artifacts()
    app.run(debug=True)