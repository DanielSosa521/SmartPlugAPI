__author__ = "Daniel Sosa"
__date__ = "April 14, 2022"

from datetime import datetime
import calendar
import random
from pymongo import MongoClient

#NOTE : Need this package for MongoClient init
#Without it, SSL CERTIFICATE VERIFY FAILED EXCEPTION
#Should find a better solution but i got fed up lol
import certifi
import database

from flask import Flask, jsonify
from flask_restful import Api, Resource
app = Flask(__name__)
api = Api(app)

CONNECTION_STRING = database.getConnectionString()
client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

db = client.SmartPlugDatabase
users = db.users
plugs = db.plugs


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

class DashboardPlugs(Resource):
    def get(self):
        print("Providing plug data\n")
        plugCount = 4                           #Hardcoding 4 plugs for testing
        points = []
        for plug in range(plugCount):
            plugPower = random.randint(0,15)        #Each plug = random power from 0 to 15
            points.append(plug)
            points.append(plugPower)
        print(points)
        return {
            'points' : points
        }

api.add_resource(DashboardPlugs, "/dashboard/plugs")

class Database(Resource):
    def get(self):
        print("Displaying database information")
        print ("Collections:\n")
        collections = []
        for c in db.list_collection_names():
            collections.append(c)                       #Add collection name to list
            # coll = db[c]      //access that collection
            
        return {
            'collections' : collections
        }
        
api.add_resource(Database, "/database")

class Register(Resource):
    def post(self, email, username, password, confpassword):
        print(email)
        print(username)
        print(password)
        print(confpassword)
        return {
            'status' : 'good'
        }

api.add_resource(Register, "/register/<string:email>/<string:username>/<string:password>/<string:confpassword>")

class Login(Resource):
    def post(self, username, password):
        print(username)
        print(password)
        return {
            'status' : 'good'
        }

api.add_resource(Login, "/login/<string:username>/<string:password>")

if __name__ == "__main__":
    app.run(debug=True)