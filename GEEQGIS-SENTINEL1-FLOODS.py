import ee 
from ee_plugin import Map 

#Import country boundaries feature collection.
dataset = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017')

#Apply filter where country name equals Pakistan.
pakistan = dataset.filter(ee.Filter.eq('country_na', 'Pakistan'))

Map.centerObject(pakistan, 9);

#Filter the collection for the VV product before flood
collectionBef = ee.ImageCollection('COPERNICUS/S1_GRD')\
    .filter(ee.Filter.eq('instrumentMode', 'IW'))\
    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))\
    .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))\
    .filterDate('2022-06-01','2022-06-30')\
    .filterBounds(pakistan)\
    .select(['VV']);

#Filter the collection for the VH product after flood
collectionAft = ee.ImageCollection('COPERNICUS/S1_GRD')\
    .filter(ee.Filter.eq('instrumentMode', 'IW'))\
    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))\
    .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))\
    .filterDate('2022-08-01','2022-08-31')\
    .filterBounds(pakistan)\
    .select(['VH']);

before = collectionBef.median().clip(pakistan);
Map.addLayer(before, {'min': -14, 'max': -7}, 'Before');

after = collectionAft.median().clip(pakistan);
Map.addLayer(after, {'min': -14, 'max': -7}, 'After');

#Mengurangi noise (radar speckle) dengan smoothing  
smoothing_radius = 100;
before_filtered = before.focal_mean(smoothing_radius, 'circle', 'meters');
after_filtered = after.focal_mean(smoothing_radius, 'circle', 'meters');

Map.addLayer(before_filtered, {'min':-25, 'max':0}, 'Before_filtered');
Map.addLayer(after_filtered, {'min':-25, 'max':0}, 'After_filtered');

#Calculate the difference between the before and after images
difference = after_filtered.divide(before_filtered);
Map.addLayer(difference,{'min':0, 'max':2},"Difference Layer");

#Apply the predefined difference-threshold and create the flood extent mask 
threshold = 1.5;
difference_binary = difference.gt(threshold);

#Refine flood result using additional datasets
#Include JRC layer on surface water seasonality to mask flood pixels from areas
#of "permanent" water (where there is water > 10 months of the year)
swater = ee.Image('JRC/GSW1_0/GlobalSurfaceWater').select('seasonality');
swater_mask = swater.gte(10).updateMask(swater.gte(10));
      
#Flooded layer where perennial water bodies (water > 10 mo/yr) is assigned a 0 value
flooded_mask = difference_binary.where(swater_mask,0);
#final flooded area without pixels in perennial waterbodies
flooded = flooded_mask.updateMask(flooded_mask);
      
#Compute connectivity of pixels to eliminate those connected to 10 or fewer neighbours
#This operation reduces noise of the flood extent product 
connections = flooded.connectedPixelCount();    
flooded = flooded.updateMask(connections.gte(10));
      
#Mask out areas with more than 5 percent slope using a Digital Elevation Model 
DEM = ee.Image('WWF/HydroSHEDS/03VFDEM');
terrain = ee.Algorithms.Terrain(DEM);
slope = terrain.select('slope');
flooded = flooded.updateMask(slope.lt(5));

Map.addLayer(flooded,{palette:"0000FF"},'Flooded areas');
