# cycle_safe(berlin)

helping to keep you and your bike safe


## Motivation

Almost 85% of Berliner's own a bike. This project addresses the issue of safety of Berlin cyclists and their bikes.


## Product

The product contains 4 key elements:
- Locations - mapping of bike distribution in Berlin
- Accidents - mapping of bike accidents & their hot spots 
- Thefts - bike theft data analysis & forecasting next day's bike theft number
- Berlin bike tweets - lates tweets about bikes in Berlin

Link to the app: https://share.streamlit.io/hmichinaka/berlin-bike-theft-forecasting/app.py

## Methods used

Machine Learning (DBSCAN cluster analysis of accidents in Berlin)
Data Analysis
Data Visualization (exploratory data analysis incl. mapping with plotly.express & folium) 
Predictive Modeling (forecasting next day's bike theft count in Berlin with time series RNN/LSTM model)
APIs (fetiching NextBike data for "Locations" part; obtaining latest bike tweets via Twitter API)
Streamlit (app was deployed via Streamlit Cloud)

## Repository overview


## Running instructions


## About

This project was the final project of 6 students who attended a Data Science bootcamp at Le Wagon Berlin between January-March 2022.

## Data Sources

**Polizei Berlin:** https://www.internetwache-polizei-berlin.de/vdb/Fahrraddiebstahl.csv

**Data Source Lebensweltlich orientierte Räume (LOR) in Berlin:** https://www.stadtentwicklung.berlin.de/planen/basisdaten_stadtentwicklung/lor/de/download.shtml

**Data source accidents:**
https://daten.berlin.de/datensaetze/strassenverkehrsunf%C3%A4lle-nach-unfallort-berlin-2018
https://daten.berlin.de/datensaetze/strassenverkehrsunf%C3%A4lle-nach-unfallort-berlin-2019
https://daten.berlin.de/datensaetze/strassenverkehrsunf%C3%A4lle-nach-unfallort-berlin-2020

**Data Source Bezirke:** https://daten.odis-berlin.de/de/dataset/bezirksgrenzen/

**Data source Nextbike:** https://sharedmobility.github.io/Nextbike.html

Data source GreenLane Project: https://www.infravelo.de/api/
