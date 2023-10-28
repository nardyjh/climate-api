# Climate Analysis and API Development

## Overview
This project involves conducting a climate analysis of Honolulu, Hawaii and developing a Flask API based on the analysis results. It includes two main parts: data analysis using Python and SQLAlchemy and creating a web API with Flask.

## Part 1: Analyze and Explore the Climate Data
In this part, we used Python, SQLAlchemy, Pandas, and Matplotlib to analyze and explore the climate database. The following steps were performed:

1. Connect to the SQLite database using SQLAlchemy.
2. Reflect the tables and save references to the "measurement" and "station" tables.
3. Conducted a precipitation analysis:
    - Found the most recent date in the dataset.
    - Retrieved the previous 12 months of precipitation data.
    - Loaded the query results into a Pandas DataFrame and plotted the results.
    - Calculated summary statistics for the precipitation data.

4. Conducted a station analysis:
    - Calculated the total number of stations.
    - Identified the most active station by listing stations and observation counts.
    - Calculated the lowest, highest, and average temperatures for the most active station.
    - Plotted temperature observations as a histogram.

## Part 2: Design Climate App
In this part, we designed a Flask API based on the queries developed in Part 1. The API offers several routes to access climate data:

- `/api/v1.0/precipitation`: Returns the last 12 months of precipitation data as a JSON dictionary.
- `/api/v1.0/stations`: Returns a list of stations from the dataset as a JSON list.
- `/api/v1.0/tobs`: Queries the dates and temperature observations of the most active station for the previous year and returns a JSON list of temperature observations.
- `/api/v1.0/<start>`: Accepts a start date as a parameter and returns JSON data with the minimum, average, and maximum temperatures calculated from the start date to the end of the dataset.
- `/api/v1.0/<start>/<end>`: Accepts start and end dates as parameters and returns JSON data with the temperature statistics calculated for the specified date range.

## Project Structure
- `climate-starter.ipynb`: Jupyter Notebook containing the initial data analysis.
- `app.py`: Python script that defines the Flask application and API routes.
- `Resources/`: Directory containing the CSV files and SQLite database file (`hawaii.sqlite`) used for the analysis.

## Dependencies
- Python
- Flask
- SQLAlchemy
- Pandas
- Matplotlib

## Usage
1. Clone this repository to your local machine.
2. Ensure you have the necessary dependencies installed.
3. Run `app.py` to start the Flask application.
4. Access the provided routes to retrieve climate data in JSON format.

## Closing Notes
This project demonstrates how to perform climate analysis and create a web API using Flask, providing easy access to climate data. Feel free to explore the provided routes and enhance the functionality as needed for your specific use case.

For any questions or improvements, please contact Jorge Nardy.

Enjoy your exploration of Honolulu's climate data!

## Acknowledgments 
Data provided by University of Toronto. 
