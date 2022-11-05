from googlemaps import client
from googlemaps import geocoding
from googlemaps import maps
import numpy as np
import cv2 as cv

# Template for features : {"feature":"FEATURE|element:ELEMENT|STYLE1|STYLE2|..."}
# Read the following to know the available FEATURES, ELEMENTS and STYLES 
# All informations on https://developers.google.com/maps/documentation/maps-static/styling
FEATURES = {'all','administrative','administrative.country', 'administrative.land_parcel', 'administrative.locality','administrative.neighborhood', 'administrative.province', 
            'landscape', 'landscape.man_made', 'landscape.natural', 'landscape.natural.landcover', 'landscape.natural.terrain', 
            'poi', 'poi.attraction', 'poi.business', 'poi.government', 'poi.medical', 'poi.park', 'poi.place_of_worship', 'poi.school', 'poi.sports_complex',
            'road', 'road.arterial', 'road.highway', 'road.highway.controlled_access', 'road.local',
            'transit', 'transit.line', 'transit.station', 'transit.station.airport', 'transit.station.bus', 'transit.station.rail'}
ELEMENTS = {'all', 'geometry', 'geometry.fill', 'geometry.fill',
            'labels', 'labels.icon', 'labels.text', 'labels.text.fill', 'labels.text.stroke'}
STYLES = {'hue', 'lightness', 'saturation', 'gamma', 'invert_lightness', 'visibility', 'color', 'weight'}


# USAGE 
# gen = imagegenerator.ImageGenerator()
# gen.GenImagebyPlaceName(addr="Grenoble", pregion="France", pzoom=15) 
# gen.GenImagebyCoords(coords=(0,0), pzoom=15) 

class ImageGenerator():
    API_KEY = None
    gclient = None

    @staticmethod
    def setup():
        ImageGenerator.API_KEY = ''
        ImageGenerator.gclient = client.Client(ImageGenerator.API_KEY)

    def __checkSetup():
        if  (ImageGenerator.API_KEY == None and ImageGenerator.gclient == None):
            print('Please call the @setup function before using ImageGenerator\'s class other functions')
            quit()

    @staticmethod
    def GenImagebyPlaceName(imageName="img.jpg", size=10000, addr=None, pplace_id=None,pcomponent=None, pbounds=None, pregion=None, 
                            plang=None, pzoom=14, mtype='roadmap', features={"feature":"all|element:labels|visibility:off"}):
            ImageGenerator.__checkSetup()
            # More details on the usage of the following function https://github.com/googlemaps/google-maps-services-python/blob/master/googlemaps/geocoding.py
            data = geocoding.geocode(client=ImageGenerator.gclient, address=addr, place_id=pplace_id, components=pcomponent, bounds=pbounds, region=pregion, language=plang )
            if not data:
                print("Please be more specific, this address either does not exist or is not unique")
                quit()
            coords = data[0]['geometry']['location']
        
            f = open(imageName, 'wb')
            for chunk in maps.static_map(client=ImageGenerator.gclient, size=size, center=coords, zoom=pzoom, maptype=mtype, style=features):
                if chunk:
                    f.write(chunk)
            f.close()
            return f

    @staticmethod
    def GenImagebyCoords(imageName="img.jpg", size=10000, coords=None, pzoom=14, mtype='roadmap', features={"feature":"all|element:labels|visibility:off"}):
        ImageGenerator.__checkSetup()
        f = open(imageName, 'wb')
        for chunk in maps.static_map(client=ImageGenerator.gclient, size=size, center=coords, zoom=pzoom, maptype=mtype, style=features):
            if chunk:
                f.write(chunk)
        f.close()
        return f


