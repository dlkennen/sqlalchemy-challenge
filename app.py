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
    return 

@app.route("/stations")
def stations():
    return 

@app.route("/tobs")
def tobs():
    return 

@app.route("/start")
def start():
    return 

@app.route("/start/end")
def start():
    return 

if __name__ == "__main__":
    app.run(debug=True)
