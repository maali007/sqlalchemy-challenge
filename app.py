import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    mr_date = dt.date(2017, 8 ,23)
    last12 = mr_date - dt.timedelta(days=365)
    session = Session(engine)
    pptn = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date.between(last12, mr_date)).all()
    session.close()
    date_pptn = {date: prcp for date, prcp in pptn}
    return jsonify(date_pptn)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    all_stations = session.query(Station.station).all()
    session.close()
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    mr_date = dt.date(2017, 8 ,23)
    last12 = mr_date - dt.timedelta(days=365)
    session = Session(engine)
    tempo = session.query(Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date.between(last12, mr_date)).all()
    session.close()
    return jsonify(tempo)

if __name__ == "__main__":
    app.run(debug=True)