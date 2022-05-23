from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from flask_app.models import user

class Car:
    db = "ev_schema"

    def __init__(self, data):
        self.id = data["id"]

        self.brand = data["brand"]
        self.model = data["model"]
        self.purchased_date = data["purchased_date"]
        self.description = data["description"]
        self.user_id = data["user_id"]

        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.user = {}

    @staticmethod
    def validate_car(data):
        is_valid = True
        if len(data["brand"])<3:
            flash("Brand must be at least 2 characters long!")
            is_valid = False
        if len(data["model"])<3:
            flash("Model must be at least 2 characters long!")
            is_valid = False
        if len(data["description"])<3:
            flash("Description must be at least 3 characters long!")
            is_valid = False

        return is_valid
    
    @classmethod
    def create_car(cls, data):
        query = "INSERT INTO cars (brand, model, purchased_date, description, user_id, created_at) VALUES (%(brand)s, %(model)s, %(purchased_date)s, %(description)s, %(user_id)s, NOW());"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cars LEFT JOIN users ON cars.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)

        all_cars = []

        for row in results:
            car = cls(row)

            user_data={
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }

            car.user = user.User(user_data)
            all_cars.append(car)

        return all_cars

    @classmethod
    def get_car_with_user(cls, data):
        query = "SELECT * FROM cars LEFT JOIN users ON cars.user_id = users.id WHERE cars.id = %(car_id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)

        car = cls(results[0])

        user_data = {
            "id": results[0]["users.id"],
            "first_name": results[0]["first_name"],
            "last_name": results[0]["last_name"],
            "email": results[0]["email"],
            "password": results[0]["password"],
            "created_at": results[0]["users.created_at"],
            "updated_at": results[0]["users.updated_at"]
        }

        car.user = user.User(user_data)
        return car

    @classmethod
    def update_car_info(cls,data):
        query = "UPDATE cars SET brand = %(brand)s, model = %(model)s, purchased_date = %(purchased_date)s, description = %(description)s, updated_at = NOW() WHERE id = %(car_id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return

    @classmethod
    def delete_car(cls, data):
        query = "DELETE FROM cars WHERE id = %(car_id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return