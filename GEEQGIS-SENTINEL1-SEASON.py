import ee 
from ee_plugin import Map 

#Defining study area and create buffer    
roi = ee.Geometry.Point(112.59,-8.09).buffer(10000);

#Filter the collection for the VV product from the descending track
collectionVV = ee.ImageCollection('COPERNICUS/S1_GRD')\
    .filter(ee.Filter.eq('instrumentMode', 'IW'))\
    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))\
    .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))\
    .filterBounds(roi)\
    .select(['VV']);

#Filter the collection for the VH product from the descending track
collectionVH = ee.ImageCollection('COPERNICUS/S1_GRD')\
    .filter(ee.Filter.eq('instrumentMode', 'IW'))\
    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))\
    .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))\
    .filterBounds(roi)\
    .select(['VH']);

#Center to ROI
Map.centerObject(roi, 13);

#Create a 3 band stack by selecting from different periods (months)
VV1 = ee.Image(collectionVV.filterDate('2022-01-01', '2022-04-30').median());
VV2 = ee.Image(collectionVV.filterDate('2022-05-01', '2022-08-31').median());
VV3 = ee.Image(collectionVV.filterDate('2022-09-01', '2022-12-31').median());

composite = VV1.addBands(VV2).addBands(VV3)

#Add to canvas
Map.addLayer(composite.clip(roi), {'min': -12, 'max': -7}, 'Season composite');