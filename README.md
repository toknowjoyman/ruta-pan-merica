# ruta-panomerica
Provides a visual interface for the database hosted on scenicroute.info


________________________________________________________________________________
rutascenic documentation
========================

Description
-----------------
rutascenic is an application that allows users to find scenic route alternatives
to their journey.
it currently works with the dataset of 850 designated scenic routes in US (federal and state)


Installation/Libraries
-------------
- Install Python 3
- Install PyQt5
- Install Folium: 
  ’pip install folium’
- include geocoder
- include polyline

Run rutascenic.py

Program Structure
-----------------
# rutascenic.py
- QMainWindow
- QWebEngineView
- Graphopper API requests
- StreetView API requests

# scenicroutemodel.py
- Scenic Route DB

## html/popup.js
- QtWebChannel interactive




PyQt application
Folium
Javascript Mapping
Leaflet
