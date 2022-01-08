import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify
import pandas as pd

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Stations = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    return (
    "Welcome to the Climate App</br>"
    "You can click any of the following: </br>"
    f"/api/v1.0/precipitation</br>"
    f"/api/v1.0/stations</br>"
    f"/api/v1.0/tobs</br>"
    f"/api/v1.0/start</br>"
    f"/api/v1.0/start/end</br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    prcplist = []

    for date, prcp in results:
        dict = {}
        dict['date'] = date
        dict['precipitation'] = prcp
        prcplist.append(dict)

    session.close()

    return jsonify(prcplist)
    
@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
    results = session.query(Measurement.station).distinct().all()
    
    stnlist = list(np.ravel(results))

    session.close()

    return jsonify(stnlist)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)
    
    active = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    most_active = active[0][0]
    
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station==most_active).filter(Measurement.date >= '2016-08-24').all()

    tempslist = []
    for date, tobs in results:
        dict = {}
        dict['date'] = date
        dict['temperature'] = tobs
        tempslist.append(dict)

    session.close()

    return jsonify(tempslist)



# @app.route("/api/v1.0/<start>")
# def start(start):



# @app.route("/api/v1.0/<start>/<end>")
# def start_end(start, end):
    
            

if __name__ == "__main__":
    app.run(debug=True)