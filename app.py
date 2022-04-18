__author__ = "Daniel Sosa"
__date__ = "April 14, 2022"

from datetime import datetime
import calendar
import random

from flask import Flask, jsonify
from flask_restful import Api, Resource
app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {"data":"Hello World"}

api.add_resource(HelloWorld, "/helloworld")

class Home(Resource):
    def get(self):
        currentMonth = datetime.now().month
        month = calendar.month_name[currentMonth]
        summary = "Energy usage looks good"
        moneysaved = random.randint(-200,200)
        powersaved = moneysaved * 27
        savings = "$"+str(moneysaved)+" : "+str(powersaved)+"KWH"
        delta = random.randint(-15,20)
        plugs = ["plug1","plug2","plug4"]
        return {
            'month':month,
            'summary':summary,
            'savings':savings,
            'delta':delta,
            'plugs':plugs
        }

api.add_resource(Home, "/home")

class DashboardMonth(Resource):
    def get(self):
        print("Providing Month Data\n")
        points = []
        samples = datetime.now().day        #Samples = day of month
        for day in range(samples):
            pwr = random.randint(400,800)
            points.append(day)
            points.append(pwr)
        print(points)
        return {
            'points':points
        }

api.add_resource(DashboardMonth, "/dashboard/month")

class DashboardDay(Resource):
    def get(self):
        print("Providing Day Data\n")
        points = []
        samples = datetime.now().hour       #Samples = current hour in 24 hour format (noon = 12, 5 pm = 17)
        for day in range(samples):
            pwr = random.randint(0,25)
            points.append(day)
            points.append(pwr)
        print(points)
        return {
            'points':points
        }

api.add_resource(DashboardDay, "/dashboard/day")

if __name__ == "__main__":
    app.run(debug=True)