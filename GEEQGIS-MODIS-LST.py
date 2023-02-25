import ee 
from ee_plugin import Map 

#Defining study area
Madagascar = ee.FeatureCollection('FAO/GAUL/2015/level2').filter(ee.Filter.inList('ADM0_NAME', ['Madagascar']));

#Defining datasets
dataset = ee.ImageCollection('MODIS/061/MOD11A1').filter(ee.Filter.date('2019-01-01', '2019-01-31'));
modis = dataset.select('LST_Day_1km');
total = modis.reduce(ee.Reducer.mean());
lst = total.clip(Madagascar)

#Visualization parameters
palette = ['040274', '040281', '0502a3', '0502b8', '0502ce', '0502e6',
    '0602ff', '235cb1', '307ef3', '269db1', '30c8e2', '32d3ef',
    '3be285', '3ff38f', '86e26f', '3ae237', 'b5e22e', 'd6e21f',
    'fff705', 'ffd611', 'ffb613', 'ff8b13', 'ff6e08', 'ff500d',
    'ff0000', 'de0101', 'c21301', 'a71001', '911003']
visParamsK = {'min':14000, 'max': 16000, 'palette': palette}

#Convert to Celsius
modisc = lst.multiply(0.02).subtract(273.15)

#Visualization parameters
palette = ['blue', 'limegreen', 'yellow', 'darkorange', 'red']
visParamsC = {'min': 20, 'max': 40, 'palette': palette}

# Zoom to an area of interest.
Map.centerObject(Madagascar, 7);

#Add clipped image layer to the map.
Map.addLayer(lst, visParamsK,  'Mean temperature of Jan 2019 (Kelvin)');
Map.addLayer(modisc, visParamsC, 'Mean temperature of Jan 2019 (Celcius)')