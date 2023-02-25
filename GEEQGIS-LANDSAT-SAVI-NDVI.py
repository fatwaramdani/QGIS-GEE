import ee 
from ee_plugin import Map 

#Defining study area
Madagascar = ee.FeatureCollection('FAO/GAUL/2015/level2').filter(ee.Filter.inList('ADM0_NAME', ['Madagascar']));

#Filter the L8 collection to a single month.
collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_RT_TOA') \
    .filterDate('2022-11-01', '2022-12-01')

#Map an expression over a collection.
#A function to compute NDVI.
def NDVI(image):
  return image.expression('float(b("B5") - b("B4")) / (b("B5") + b("B4"))')

#A function to compute SAVI.
def SAVI(image):
  return image.expression(
      '(1 + L) * float(nir - red)/ (nir + red + L)',
      {
        'nir': image.select('B5'),
        'red': image.select('B4'),
        'L': 0.2
      })

#Visualization parameters.
vis = {
  'min': 0,
  'max': 1,
  'palette': [
      'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718',
      '74A901', '66A000', '529400', '3E8601', '207401', '056201',
      '004C00', '023B01', '012E01', '011D01', '011301'
  ]
}

#Zoom to an area of interest.
Map.centerObject(Madagascar, 7);

#Computes the mean NDVI and SAVI and clip to the study area.
meanNDVI = collection.map(NDVI).mean().clip(Madagascar)
meanSAVI = collection.map(SAVI).mean().clip(Madagascar)

#Map and display.
Map.addLayer(meanNDVI, vis, 'Mean NDVI')
Map.addLayer(meanSAVI, vis, 'Mean SAVI')
