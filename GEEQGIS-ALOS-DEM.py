import ee 
from ee_plugin import Map 

#Load admin boundary
Madagascar = ee.FeatureCollection('FAO/GAUL/2015/level2').filter(ee.Filter.inList('ADM0_NAME', ['Madagascar']));

# Load JAXA elevation image.
dataset = ee.Image('JAXA/ALOS/AW3D30/V2_2');
elev = dataset.select('AVE_DSM')

#Clip LULC data based on admin boundary
data_clip = elev.clip(Madagascar);

# Use the terrain algorithms to compute a hillshade with 8-bit values.
shade = ee.Terrain.hillshade(data_clip)
Map.addLayer(shade, {}, 'hillshade')

# Create a "sea" variable to be used for cartographic purposes
sea = data_clip.lte(0)
Map.addLayer(sea.mask(sea), {'palette':'000022'}, 'sea', 0)

# Create a custom elevation palette from hex strings.
elevationPalette = ['006600', '002200', 'fff700', 'ab7634', 'c4d0ff', 'ffffff']
# Use these visualization parameters, customized by location.
visParams = {'min': 1, 'max': 3000, 'palette': elevationPalette}

# Create a mosaic of the sea and the elevation data
visualized = ee.ImageCollection([
  # Mask the elevation to get only land
  data_clip.mask(sea.Not()).visualize(**visParams),
  # Use the sea mask directly to display sea.
  sea.mask(sea).visualize(**{'palette':'000022'})
]).mosaic()

# Note that the visualization image doesn't require visualization parameters.
Map.addLayer(visualized, {}, 'elevation palette')

# Convert the visualized elevation to HSV, first converting to [0, 1] data.
hsv = visualized.divide(255).rgbToHsv()
# Select only the hue and saturation bands.
hs = hsv.select(0, 1)
# Convert the hillshade to [0, 1] data, as expected by the HSV algorithm.
v = shade.divide(255)
# Create a visualization image by converting back to RGB from HSV.
# Note the cast to byte in order to export the image correctly.
rgb = hs.addBands(v).hsvToRgb().multiply(255).byte()
Map.addLayer(rgb, {}, 'styled')

# Zoom to an area of interest.
Map.centerObject(Madagascar, 6);