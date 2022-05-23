from flask_app import app
from flask import render_template, redirect, session, request, flash

from flask_app.models.car import Car

#=============================================
#Create Car Route
#=============================================
@app.route("/new_car")
def new_car():
    if "user_id" not in session:
        flash("Please login or register before entering site!")
        return redirect("/")
    return render_template("new_car.html")

@app.route("/create_car", methods = ["POST"])
    #1 - validate form data
def create_car():
    data={
    "brand": request.form["brand"],
    "model": request.form["model"],
    "purchased_date": request.form["purchased_date"],
    "description": request.form["description"],
    "user_id": session["user_id"]
}

    if not Car.validate_car(data):
        return redirect("/new_car")

    #2 - save new car to database
    Car.create_car(data)


    #3 - redirect to the dashboard
    return redirect ("/dashboard")

#=============================================
#Create One Car Route
#=============================================

@app.route("/car/<int:car_id>")
def display_car(car_id):
    if "user_id" not in session:
        flash("Please login or register before entering site!")
        return redirect("/")
  
    #1 - query for car info w/ associated info of user
    data = {
        "car_id": car_id
    }
    car = Car.get_car_with_user(data)


    return render_template("display_car.html", car = car)

#=============================================
#Edit One Car Route
#=============================================

@app.route("/car/edit/<int:car_id>")
def edit_car(car_id):
    #1, query for the car we want to update
    data = {
        "car_id": car_id
    }
    car = Car.get_car_with_user(data)

    #2, pass car info to the html
    return render_template("edit_car.html", car = car)

@app.route("/car/<int:car_id>/update", methods = ["POST"])
def update_car(car_id):
    #1 - validate our form data

    data={
        "brand": request.form["brand"],
        "model": request.form["model"],
        "purchased_date": request.form["purchased_date"],
        "description": request.form["description"], 
        "car_id": car_id
    }

    if not Car.validate_car(data):
        return redirect(f"/car/edit/{car_id}")

    #2, udpate info
    Car.update_car_info(data)

    #redirect
    return redirect("/dashboard")
        
        #=============================================
#Delete One car Route
#=============================================
@app.route("/car/delete/<int:car_id>")
def delete_car(car_id):
    data = {
        "car_id": car_id
    }
    Car.delete_car(data)

    return redirect("/dashboard")
    