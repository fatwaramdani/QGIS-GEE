import ee
from ee_plugin import Map

#Defining study area
boundary = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017");
country = boundary.filterMetadata('country_na','equals','Nigeria');

#Defining the datasets and clip to study area
data = ee.ImageCollection("COPERNICUS/S2_HARMONIZED")\
        .filterDate("2022-01-01", "2022-03-31")\
        .filterBounds(country)
s2composite = data.median().clip(country)

#Visualization parameters
trueColour = {'bands': ["B11", "B8", "B2"], 'min': 0, 'max': 6000, 'gamma': 1.5}

#Map and display 
Map.addLayer(s2composite, trueColour, "Nigeria-Sentinel, 2022")
Map.centerObject(country, 7)
