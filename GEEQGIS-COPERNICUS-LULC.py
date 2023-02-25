import ee 
from ee_plugin import Map 

#Load admin boundary
Nigeria = ee.FeatureCollection('FAO/GAUL/2015/level2').filter(ee.Filter.inList('ADM0_NAME', ['Nigeria']));

#Load Copernicus data
dataset = ee.Image("COPERNICUS/Landcover/100m/Proba-V-C3/Global/2019").select('discrete_classification');

#Clip LULC data based on admin boundary
data_clip = dataset.clip(Nigeria);

#Visualize the image
Map.centerObject(Nigeria, 7);
Map.addLayer(data_clip, {}, "Land Cover Nigeria");
