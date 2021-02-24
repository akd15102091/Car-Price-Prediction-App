from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("rf_random_model.pkl", "rb"))



@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")




@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":

        # X_test columns : -
        # ['Present_Price', 'Kms_Driven', 'Owner', 'no_year', 'Fuel_Type_Diesel',
        #  'Fuel_Type_Petrol', 'Seller_Type_Individual', 'Transmission_Manual']



        year = int(request.form['year'])
        no_year = 2020 - year

        Present_Price = float(request.form["Present_Price"])

        Kms_Driven = int(request.form["Kms_Driven"])

        Owner = int(request.form["Owner"])

        FuelType = request.form["FuelType"]
        Fuel_Type_Diesel = 0
        Fuel_Type_Petrol = 0

        if(FuelType=="Diesel") :
            Fuel_Type_Diesel = 1

        elif(FuelType=="Petrol") :
            Fuel_Type_Petrol = 1


        SellerType = request.form["SellerType"]
        Seller_Type_Individual = 0
        if(SellerType=="Individual") :
            Seller_Type_Individual = 1


        TransmissionType = request.form["TransmissionType"]
        Transmission_Manual = 0
        if(TransmissionType=="Manual Car") :
            Transmission_Manual = 1


        
        prediction=model.predict([[Present_Price, Kms_Driven, Owner, no_year, Fuel_Type_Diesel,
        Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Manual]])


        output=round(prediction[0],2)

        return render_template('home.html',prediction_text="Selling Price :  {} Lacs".format(output))


    return render_template("home.html")




if __name__ == "__main__":
    app.run(debug=True)
