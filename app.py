#SQL Alchemy HW for Diana Kennen

#Set up dependencies
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

from flask import Flask, jsonify

#Setup Database
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Station = Base.classes.station
Measurement = Base.classes.measurement

#Setting Up Flask
app = Flask(__name__)

#Setting up Flask Routes for homepage

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/<start><br/>"
        f"/api/v1.0/temp/<start>/<end>"
    )

#Precipitation Route

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Create session link
    session = Session(engine)

    # Perform a query to retrieve the data and precipitation scores
    precip = session.query(Measurement.prcp, Measurement.date).\
            filter(Measurement.date > '2016-08-23').\
            order_by(Measurement.date).all()

    session.close()

    #Create dictionary of dates and precipitation
    all_precip = []
    for prcp, date in precip:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        all_precip.append(precip_dict)
    return jsonify(all_precip)

#Station Route

@app.route("/api/v1.0/stations")
def stations():
    #Create session link
    session = Session(engine)

    #Query list of stations
    stations = session.query(Station.station).all()

    session.close()

    #Convert to normal list
    station_list = list(np.ravel(stations))
    
    return jsonify(station_list)

#Temperature Route

@app.route("/api/v1.0/tobs")
def tobs():
    #Create session link
    session = Session(engine)

    #Query list of stations
    temps = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281')

    session.close()

    #Create list of temperatures
    temp_list = []
    for t in temps:
        if type(t.tobs) == float:
            temp_list.append(t.tobs)

    return jsonify(temp_list)

#Start Date Route

@app.route("/api/v1.0/temp/<start>")
def start(start):
    
    start_date = start
    
    session = Session(engine)

    # Using the most active station id and start date, calculate the lowest, highest, and average temperature.
    station_pick = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= start_date)
    
    session.close()
    
    #Eliminating missing data
    temp_list = []
    for t in station_pick:
        if type(t.tobs) == float:
            temp_list.append(t.tobs)
    
    #Store minimum temperature
    minT = min(temp_list)
    
    #Store maximum temperature
    maxT = max(temp_list)

    #Importing mean function
    from statistics import mean

    #Computing mean and storing
    meanT = round(mean(temp_list), 2)     

    #Creating a dictionary of these values
    Dict = {'Start Date': start_date, 'Min Temp deg F': minT, 'Max Temp deg F': maxT, 'Mean Temp deg F': meanT}

    return jsonify(Dict)

#Start and End Date Route

@app.route("/api/v1.0/temp/<start>/<end>")
def end(start):
    start_date = start
    end_date = end
    
    session = Session(engine)

     # Using the most active station id and start date, calculate the lowest, highest, and average temperature.
    station_pick = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date)
    
    session.close()
    
    #Eliminating missing data
    temp_list = []
    for t in station_pick:
        if type(t.tobs) == float:
            temp_list.append(t.tobs)
    
    #Store minimum temperature
    minT = min(temp_list)
    
    #Store maximum temperature
    maxT = max(temp_list)

    #Importing mean function
    from statistics import mean

    #Computing mean and storing
    meanT = round(mean(temp_list), 2)     

    #Creating a dictionary of these values
    Dict = {'Start Date': start_date, 'End Date': end_date, 'Min Temp deg F': minT, 'Max Temp deg F': maxT, 'Mean Temp deg F': meanT}
    
    return jsonify(Dict)

if __name__ == "__main__":
    app.run(debug=True)
