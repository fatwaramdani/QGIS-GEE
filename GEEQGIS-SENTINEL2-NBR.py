import ee
from ee_plugin import Map

#Defining study area and create buffer    
point = ee.Geometry.Point(112.59, -7.75).buffer(10000);
Map.centerObject(point, 11);

#Defining datasets
s2 = ee.ImageCollection('COPERNICUS/S2_HARMONIZED')\
    .select(['B2', 'B3', 'B4', 'B8', 'B11', 'B12'],\
        ['blue', 'green', 'red', 'nir', 'swir1', 'swir2']);

#Before forest fire
preImage = s2\
    .filterBounds(point)\
    .filterDate('2019-06-20', '2019-06-30')\
    .sort('CLOUD_COVERAGE_ASSESSMENT')\
    .first();

#After forest fire    
postImage = s2\
    .filterBounds(point)\
    .filterDate('2019-10-20', '2019-10-31')\
    .sort('CLOUD_COVERAGE_ASSESSMENT')\
    .first();

#Vizualization parameters for RGB combinations
visParam = {\
    'bands': ['swir2', 'swir1', 'green'],\
    'min': 0,\
    'max': 3000\
};

Map.addLayer(preImage.clip(point), visParam, 'pre');
Map.addLayer(postImage.clip(point), visParam, 'post');

#Calculate NBR.
nbrPre = preImage.normalizedDifference(['nir', 'swir2'])\
    .rename('nbr_pre');
nbrPost = postImage.normalizedDifference(['nir', 'swir2'])\
    .rename('nbr_post');
    
#Calculate change.
diff = nbrPost.subtract(nbrPre).rename('change');

palette = [\
    '011959', '0E365E', '1D5561', '3E6C55', '687B3E',\
    '9B882E', 'D59448', 'F9A380', 'FDB7BD', 'FACCFA'\
];

#Vizualization parameters for dNBR
visParams = {\
    'palette': palette,\
    'min': -1,\
    'max': 1\
};

#Display the result, clip to study area
Map.addLayer(diff.clip(point), visParams, 'change');

#Classify change 
thresholdGain = 0.5;
thresholdLoss = -0.50;

diffClassified = ee.Image(0);

diffClassified = diffClassified.where(diff.lte(thresholdLoss), 2);
diffClassified = diffClassified.where(diff.gte(thresholdGain), 1);

#Vizualization parameters for threshold
changeVis = {\
    'palette': ['fff70b', 'ffaf38', 'ff641b'],\
   'min': 0,\
   'max': 2\
};

#Display the final result
Map.addLayer(diffClassified.selfMask().clip(point), changeVis, 'change classified by threshold');
