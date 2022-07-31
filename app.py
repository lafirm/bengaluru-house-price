from flask import Flask,request,jsonify, app, url_for, render_template
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


def get_estimated_price(location, sqft, bath, bhk):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1
    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1
    return round(__model.predict([x])[0], 2)


@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])
    # response = jsonify({
    #     'estimated_price': get_estimated_price(location, total_sqft, bath, bhk)
    # })
    # response.headers.add('Access-Control-Allow-Origin', '*')
    result = get_estimated_price(location, total_sqft, bath, bhk)
    return render_template("app.html",prediction_text="{} Lakhs".format(result))

if __name__ == '__main__':
    print("Starting Python Flask Server for BLR Home Price Prediction")
    load_saved_artifacts()
    app.run(debug=True)






# regmodel=pickle.load(open('regmodel.pkl','rb'))
# scalar=pickle.load(open('scaling.pkl','rb'))
# @app.route('/')
# def home():
#     return render_template('home.html')
#
# @app.route('/predict_api',methods=['POST'])
# def predict_api():
#     data=request.json['data']
#     print(data)
#     print(np.array(list(data.values())).reshape(1,-1))
#     new_data=scalar.transform(np.array(list(data.values())).reshape(1,-1))
#     output=regmodel.predict(new_data)
#     print(output[0])
#     return jsonify(output[0])
#
# @app.route('/predict',methods=['POST'])
# def predict():
#     data=[float(x) for x in request.form.values()]
#     final_input=scalar.transform(np.array(data).reshape(1,-1))
#     print(final_input)
#     output=regmodel.predict(final_input)[0]
#     return render_template("home.html",prediction_text="The House price prediction is {}".format(output))
