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

Link to the app: https://cyclesafeberlin.herokuapp.com

Live presentation at Le Wagon: https://youtu.be/lyFH0OvAV9w?t=1095

## Methods used

Machine Learning (DBSCAN cluster analysis of accidents in Berlin)
Data Analysis
Data Visualization (exploratory data analysis incl. mapping with plotly.express & folium) 
Predictive Modeling (forecasting next day's bike theft count in Berlin with time series RNN/LSTM model)
APIs (fetiching NextBike data for "Locations" part; obtaining latest bike tweets via Twitter API)
Streamlit (app was deployed via Streamlit Cloud)


## Instructions to deploy online
1. Register on https://streamlit.io/cloud
2. Sign in to https://streamlit.io/cloud
3. Then fork this repository
4. Go back to Streamlit and click "New app"
5. Then click "Paste GitHub URL"
6. Copy this link "https://github.com/YOUR_GITHUB_NAME/berlin-bike-theft-forecasting/blob/master/app.py" and replace YOUR_GITHUB_NAME with yours
7. Paste it to "GitHub URL" on Streamlit
8. Click "Deploy!"
9. After a few minutes your app is live!

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

Reference code to collect live data: https://github.com/technologiestiftung/bike-sharing
