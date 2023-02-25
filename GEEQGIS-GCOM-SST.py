import ee 
from ee_plugin import Map 

dataset = ee.ImageCollection("JAXA/GCOM-C/L3/OCEAN/SST/V3").filterDate('2022-12-01', '2023-01-01').filter(ee.Filter.eq("SATELLITE_DIRECTION", "D")); # filter to daytime data only

#Multiply with slope coefficient and add offset
dataset = dataset.mean().multiply(0.0012).add(-10);

palette = ['000000', '005aff', '43c8c8', 'fff700', 'ff0000']
visParams = {'bands': 'SST_AVE', 'min':0, 'max':30, 'palette': palette}

Map.setCenter(128.45, 33.33, 5);
Map.addLayer(dataset, visParams, "Sea Surface Temperature");
