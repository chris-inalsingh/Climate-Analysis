import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt


#create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

#create session
session = Session(engine)

#Set up Flask and landing page
app = Flask(__name__)

query_date= '2016-08-22'
#Home page
@app.route("/")
def main():
   return(  f"Welcome to the Home Page<br/>"
         f"Available Routes:<br/>"
         f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
         f"/api/v1.0/tobs<br/>"
         f"/api/v1.0/start_date<br/>"
         f"/api/v1.0/start_date/end_date"
    )

 #precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year= session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > query_date).all()
    last_year_dict=dict(last_year)
    return jsonify(last_year_dict)

 #station route
@app.route("/api/v1.0/stations")
def stations():
    station_names= session.query(Station.station).all()
    return jsonify(station_names)

 #temperature route
@app.route("/api/v1.0/tobs")
def tobs():
    last12_temp = session.query(Measurement.station, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date > query_date).all()
    return jsonify(last12_temp)

 #start dynamic route
@app.route("/api/v1.0/<start>")
def start(start=None):
    start_query = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    return jsonify(start_query)
#start/end dynamic route
@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
    start_end_query=session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(start_end_query)
 #run app
if __name__ == "__main__":
    app.run(debug=True)
