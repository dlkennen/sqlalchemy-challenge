#SQL Alchemy HW for Diana Kennen
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/precipitation")
def precipitation():
    #Create session link
    session = Session(engine)

    # Perform a query to retrieve the data and precipitation scores
    precip = session.query(Measurement.prcp, Measurement.date).\
            filter(Measurement.date > '2016-08-23').\
            order_by(Measurement.date).all()

    session.close()

    all_precip = []
    for prcp, date in precip:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        all_precip.append(precip_dict)
    return jsonify(all_precip)

@app.route("/stations")
def stations():
    #Create session link
    session = Session(engine)

    #Query list of stations
    stations = session.query(Station.station).all()

    session.close()

    #Convert to normal list
    station_list = list(np.ravel(stations))
    
    return jsonify(station_list)

@app.route("/tobs")
def tobs():
    #Create session link
    session = Session(engine)

    #Query list of stations
    temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281')

    session.close()

    temp_list = []
    for date, tobs in temps:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        temp_list.append(temp_dict)
    return jsonify(temp_list)

@app.route("/<start>")
def start(start):

    start_date = str(start)

    session = Session(engine)

    # Using the most active station id and start date, calculate the lowest, highest, and average temperature.
    station_pick = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= start_date)
    
    Session.close()

    #Store minimum temperature
    minT = min(station_pick)
    
    #Store maximum temperature
    maxT = max(station_pick)

    #Eliminating missing data
    temp_list = []
    for t in station_pick:
        if type(t.tobs) == float:
            temp_list.append(t.tobs)

    #Importing mean function
    from statistics import mean

    #Computing mean and storing
    meanT = round(mean(temp_list), 2)     

    #Creating a dictionary of these values
    Dict = {'Start Date': start, 'Min Temp °F': minT, 'Max Temp °F': maxT, 'Mean Temp °F': meanT}

    return jsonify(Dict)

@app.route("/<start>/<end>")
def start_end(start, end):
    start_date = str(start)
    end_date = str(end)

    session = Session(engine)

    # Using the most active station id and start date, calculate the lowest, highest, and average temperature.
    station_pick = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date)
    
    Session.close()

    #Store minimum temperature
    minT = min(station_pick)
    
    #Store maximum temperature
    maxT = max(station_pick)

    #Eliminating missing data
    temp_list = []
    for t in station_pick:
        if type(t.tobs) == float:
            temp_list.append(t.tobs)

    #Importing mean function
    from statistics import mean

    #Computing mean and storing
    meanT = round(mean(temp_list), 2)     

    #Creating a dictionary of these values
    Dict = {'Start Date': start, 'Min Temp °F': minT, 'Max Temp °F': maxT, 'Mean Temp °F': meanT}

    return jsonify(Dict) 

if __name__ == "__main__":
    app.run(debug=True)
