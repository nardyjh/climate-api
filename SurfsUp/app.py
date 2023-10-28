# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import numpy as np
from datetime import datetime, timedelta
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

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
def homepage():
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"/api/v1.0/&lt;start&gt; (replace &lt;start&gt; with a date)<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt; (replace &lt;start&gt; and &lt;end&gt; with dates)"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query the last 12 months of precipitation data and convert to dictionary
    # Calculate date
    most_recent_date = session.query(func.max(measurement.date)).scalar()
    most_recent_date = datetime.strptime(most_recent_date, '%Y-%m-%d')
    one_year_ago = most_recent_date - timedelta(days=365)

    #Query precipitation for last 12 months
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year_ago).all()
    
    # Convert results into dictionary
    precipitation_data = {}
    for date, prcp in results:
        precipitation_data[date] = prcp 
        
    #Return JSON representation of data
    return jsonify(precipitation_data)


@app.route("/api/v1.0/stations")
def stations():
    # Query the list of stations and return as JSON
    results = session.query(station.station).all()

    #Convert results into Python list
    station_data = [result[0] for result in results]

    #Return JSON
    return jsonify(station_data)


@app.route("/api/v1.0/tobs")
def tobs():
    # Query temperature observations for the most active station for the previous year and return as JSON
    most_recent_date = session.query(func.max(measurement.date)).scalar()
    most_recent_date = datetime.strptime(most_recent_date, '%Y-%m-%d')
    one_year_ago = most_recent_date - timedelta(days=365)

    #Find most active station
    most_active_station = session.query(measurement.station, func.count(measurement.station)) \
    .group_by(measurement.station) \
    .order_by(func.count(measurement.station).desc()) \
    .first()[0]

    #Query temperature observations for most active station in last year
    results = session.query(measurement.date, measurement.tobs) \
    .filter(measurement.station == most_active_station) \
    .filter(measurement.date >= one_year_ago) \
    .all()

    #Convert results to a list of dictionaries 
    tobs_data = []
    for date, tobs in results:
        tobs_data.append({
            "date": date,
            "tobs": tobs})

    #Return JSON
    return jsonify(tobs_data)


@app.route("/api/v1.0/<start>")
def start_date(start):
    # Convert the start date string to a datetime object
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")

    # Query to calculate TMIN, TAVG, and TMAX for dates greater than or equal to the start date
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs))\
        .filter(measurement.date >= start_date).all()

    # Unpack the results
    tmin, tavg, tmax = results[0]

    # Create a dictionary with the results
    stats_data = {
        "TMIN": tmin,
        "TAVG": tavg,
        "TMAX": tmax
    }

    #Return JSON
    return jsonify(stats_data)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Convert to datetime objects
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")

    # Query database to get temperature statistics for date range
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs))\
        .filter(measurement.date >= start_date, measurement.date <= end_date).all()

    # Unpack the results
    (min_temp, avg_temp, max_temp) = results[0]

    # Create a dictionary of results
    stats_data = {
        "TMIN": min_temp,
        "TAVG": avg_temp,
        "TMAX": max_temp
    }

    #Return JSON
    return jsonify(stats_data)

