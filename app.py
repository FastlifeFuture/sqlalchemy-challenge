#Import modules
from unicodedata import name
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

# Set up your database
engine = create_engine("sqlite:///hawaii.sqlite")

#reflect an existing database into a new model
Base = automap_base()

#reflect the tables
Base.prepare(engine, reflect=True )

#Save the reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#create an app and pass __name__
app = Flask(__name__)

#Develop Flask routes for the app

#Define the home page 
@app.route("/")
def home():
   
    print("Client request was recieved")
    """All availble api routes"""
    
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end><br>")

#create route for percipitation
@app.route("/api/v1.0/precipitation")
def prcp():
    print("Client request was recieved")
    
    # create a session that will link from python to db
    session = Session(engine)
   
    #base classes keys allows you to examine the tables that hold the data
    print(Base.classes.keys())
    
    #query date and percipitation
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    #close out the session()
    session.close()
    
    # Create a dictionary from the  data and append to 
    # a list
    prcp_measurement = []
    
    #create a for loop in order to retrieve the data
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_measurement.append(prcp_dict)
   
    #return the data jsonified
    return jsonify(prcp_measurement)

#Create a route for stations
@app.route("/api/v1.0/stations")
def stations():
    print("Client request was recieved")
    
    # create a session that will link from python to db
    session = Session(engine)
    
    #base classes keys allows you to examine the tables that hold the data
    print(Base.classes.keys())
    
    #query  date and percipitation
    results = session.query(Station.station, Station.name).all()
    
    #close out the session
    session.close()
    
    # Create a dictionary from the  data and append to 
    # a list
    stations = []
    
    #create a for loop in order to retrieve the data
    for station, name in results:
        stations_dict = {}
        stations_dict["station"] = station
        stations_dict["name"] = name 
        stations.append(stations_dict)
    
    #return the data jsonified
    return jsonify(stations)

#Create a route for the most active station
@app.route("/api/v1.0/tobs")
def tobs():
    print("Client request was recieved")
    
    # create a session that will link from python to db
    session = Session(engine)
    
    #base classes keys allows you to examine the tables that hold the data
    print(Base.classes.keys())
    
    #query date and temps for the most active stattion
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281')
    
    #close out the session
    session.close()
    
    #Create a dictionary from the data and append to a list
    most_active_tobs = []
    
    #create a for loop to retrieve the data
    for date, tobs in results:
       tobs_dict = {}
       tobs_dict["date"] = date
       tobs_dict["tobs"] = tobs
       most_active_tobs.append(tobs_dict)
    
    #return the data jsonified
    return jsonify(most_active_tobs)

#Create a route that will return the min, avg, max temperature given start date or start to the end date
@app.route("/api/v1.0/<start>")
def begin_date(start = None):
    start = dt.datetime.strptime(start, "%Y-%m-%d").date()
    print("Client request was recieved")
    
    #create a session that will link from python to db
    session = Session(engine)
    
    #base classes keys allows you to examine the tables that hold the data
    print(Base.classes.keys())
    
    #query date and temps for the most active station
    
    count_max = func.max(Measurement.tobs)
    count_min = func.min(Measurement.tobs)
    count_avg = func.avg(Measurement.tobs)   
    
    results = session.query(Measurement.date, count_max, count_min, count_avg).filter(Measurement.date >= start)
   
    #close out the session
    session.close()
    
    begin_date = []
    for date, tobs in results: 
        begin_date_dict = {}
        begin_date_dict["date"] = date
        begin_date_dict["tobs"] = tobs
        begin_date.append(begin_date_dict)

    return jsonify(begin_date)

# @app.route("/api/v1.0/<start>/<end>")
# def begin_to_end_date(start = None, end = None)
#     start = dt.datetime.strptime(start, "%Y-%m-%d").date()
#     end = dt.datetime.strptime(start, "%Y-%m-%d").date()


    # Temps_df = pd.DataFrame(Temps, columns = ['date','Tobs'])
    # return(Temps_df.to_json())
if __name__ == "__main__":
    app.run(debug=True)