import ee 
from ee_plugin import Map 

#Defining study area and create buffer    
point = ee.Geometry.Point(106.85, -6.25).buffer(100000);

#Defining datasets and time range
before = ee.ImageCollection('COPERNICUS/S5P/NRTI/L3_NO2')\
  .select('NO2_column_number_density')\
  .filterDate('2019-12-01', '2019-12-31');
  
after = ee.ImageCollection('COPERNICUS/S5P/NRTI/L3_NO2')\
  .select('NO2_column_number_density')\
  .filterDate('2020-04-01', '2020-04-30');

#Visualization parameters
vizParams = {'min': 0, 'max': 0.0002, \
            'palette':['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red'],\
            'opacity': 0.7}

#Display the result
Map.addLayer(before.mean().clip(point), vizParams, 'Before COVID19');
Map.addLayer(after.mean().clip(point), vizParams, 'After COVID19');
Map.setCenter(106.85, -6.25, 9);
