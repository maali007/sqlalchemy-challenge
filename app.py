# Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd
import datetime as dt

from flask import Flask, jsonify

# Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect database into new model
Base = automap_base()

# Reflect tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask setup
app = Flask(__name__)


# Flask routes
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
    session = Session(engine)
    mr_date = dt.date(2017, 8 ,23)
    last12 = mr_date - dt.timedelta(days=365)
    pptn = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date.between(last12, mr_date)).all()
    date_pptn = {date: prcp for date, prcp in pptn}
    return jsonify(date_pptn)
    session.close()

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    all_stations = session.query(Station.station).all()
    return jsonify(all_stations)
    session.close()

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    mr_date = dt.date(2017, 8 ,23)
    last12 = mr_date - dt.timedelta(days=365)
    tempo = session.query(Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date.between(last12, mr_date)).all()
    session.close()
    return jsonify(tempo)
    session = Session(engine)

if __name__ == "__main__":
    app.run(debug=True)