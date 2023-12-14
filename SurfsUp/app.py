# Import the dependencies.
import pandas as pd
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect = True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return(
        "Welcome to the homepage of Climate API."
        "***"
        "Avalable routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    recent_date = dt.datetime(2017, 8, 23) - dt.timedelta(days = 365)
    results = session.query(Measurement.date, func.avg(Measurement.prcp)).\
                    filter(Measurement.date >= recent_date).all()
    precipitation = {date: prcp for date, prcp in results}
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def station():
    results = session.query(Station.station).all()
    station = list(np.ravel(results))
    return jsonify(station = station)

@app.route("/api/v1.0/tobs")
def tobs():
    recent_date = dt.datetime(2017, 8, 23) - dt.timedelta(days = 365)
    results = session.query(Measurement.station, Measurement.tobs).\
                filter(Measurement.station == "USC00519281").\
                filter(Measurement.date >= recent_date).all()
    temperature = list(np.ravel(results))
    return jsonify(temperature)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def stats(start = None, end = None):
    sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        tempurature = list(np.ravel(results))
        return jsonify(tempurature)
    
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    tempurature = list(np.ravel(results))
    return jsonify(tempurature = tempurature)

if __name__ == '__main__':
    app.run(debug=True)