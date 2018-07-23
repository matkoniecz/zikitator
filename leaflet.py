#in synch with leaflet.rb in bicycle map of krakow
#TODO - create library to DRY

def get_before(title):
    return """
<!DOCTYPE html>
<html>
<head>
	<title>""" + title + """</title>
	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0">

  <link rel=\"stylesheet\" href=\"https://unpkg.com/leaflet@1.3.3/dist/leaflet.css\"
   integrity=\"sha512-Rksm5RenBEKSKFjgI3a41vrjkw4EVPlJ3+OiI65vTjIdo9brlAacEuKOiQ5OFh7cOI1bkDwLqdLw3Zg0cRJAAQ==\"
   crossorigin=""/>
  <script src=\"https://unpkg.com/leaflet@1.3.3/dist/leaflet.js\"
   integrity=\"sha512-tAGcCfR4Sc5ZP5ZoVz0quoZDYX5aCtEm/eu1KhSLj2c9eFrylXZknQYmxUssFaVJKvvc0dJQixhGjG2yXWiV9Q==\"
   crossorigin=""></script>

       <style>
        body {
            padding: 0;
            margin: 0;
        }
        html, body, #map {
            height: 100%;
            width: 100%;
        }
    </style>
</head>
<body>
	<div id="map"></div>

	<script>
		var map = L.map('map').setView([50.07, 19.92], 13);
		mapLink = '<a href="http://openstreetmap.org">OpenStreetMap</a>';
		L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			maxZoom: 18,
			attribution: '&copy; ' + mapLink + ' Contributors'
		}).addTo(map);
"""


def get_after():
    return """
	</script>
</body>
</html>
"""


def get_location(lat, lon):
    return "[" + str(lat) + ", " + str(lon) + "]"

def get_marker(text, lat, lon):
    location = get_location(lat, lon)
    return "L.marker(" + location + ").addTo(map).bindPopup(\"" + text + ".\");\n"

def get_line(lat1, lon1, lat2, lon2, color='red'):
    location1 = get_location(lat1, lon1)
    location2 = get_location(lat2, lon2)
    return "L.polyline([" + location1 + ", " + location2 + "]," + """
		    {
                color: '""" + color + """',
                weight: 3,
                opacity: .7,
                lineJoin: 'round'
            }
            ).addTo(map);"""
