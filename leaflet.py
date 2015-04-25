def get_before(title):
    return """
<!DOCTYPE html>
<html>
<head>
	<title>""" + title + """</title>
	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.css" />
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

	<script src="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.js"></script>
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


def get_marker(text, lat, lon):
    location = "[" + str(lat) + ", " + str(lon) + "]"
    return "L.marker(" + location + ").addTo(map).bindPopup(\"" + text + ".\");\n"

