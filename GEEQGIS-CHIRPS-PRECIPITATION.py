import ee
from ee_plugin import Map

#Import country boundaries feature collection.
dataset = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017');

#Apply filter where country name equals Nigeria.
Nigeria = dataset.filter(ee.Filter.eq('country_na', 'Nigeria'));

#Add precipitation data
filtered = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY').filter(ee.Filter.date('2019-01-01', '2019-01-31')).select('precipitation');
total = filtered.reduce(ee.Reducer.mean());

#Visualization parameters
palette = ['1621a2', 'ffffff', '03ffff', '13ff03', 'efff00', 'ffb103', 'ff2300'];
visParams = {'min':0, 'max': 10, 'palette': palette};

#Visualizing the data 
Map.addLayer(total.clip(Nigeria), visParams, 'NigeriaPrecipitationJan2019');
Map.centerObject(Nigeria, 7);
