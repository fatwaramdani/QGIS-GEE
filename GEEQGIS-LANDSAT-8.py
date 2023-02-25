import ee
from ee_plugin import Map

#Defining the study area
boundary = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017");
country = boundary.filterMetadata('country_na','equals','Nigeria');

#Defining the datasets and clip to study area
data = ee.ImageCollection("LANDSAT/LC08/C02/T1_TOA")\
        .filterDate("2022-01-01", "2022-03-31")\
        .filterBounds(country)
l8composite = data.median().clip(country)

#Visualization parameters
trueColour = {'bands': ["B4", "B3", "B2"], 'min': 0.02, 'max': 0.35, 'gamma': 1.5}

#Map and display
Map.addLayer(l8composite, trueColour, "Nigeria-L8, 2022")
Map.centerObject(country, 7)
