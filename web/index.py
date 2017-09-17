from flask import Flask, Response, redirect, render_template, request, send_from_directory
from googleplaces import GooglePlaces, types, lang
import urllib2
import json
import os

app = Flask(__name__)


@app.route("/")
def index():
	ESRI_PROXY_KEY = os.environ['ESRI_PROXY_KEY']
	return render_template('index.html', ESRI_PROXY_KEY=ESRI_PROXY_KEY)

@app.route("/test")
def test():
  return json_response({'Message' : 'Some data'})

@app.route("/locations/<place>/<type>")
def locations(place, type):
	if(type.lower() == "sightseeing"):
		type = "Points of Interest"

	PLACES_API_KEY = os.environ['PLACES_API_KEY']
	places = GooglePlaces(PLACES_API_KEY)
	result = places.text_search(type + " near " + place)
	locations = []
	for place in result._places:
		locations.append([str(place._geo_location['lat']), str(place._geo_location['lng']), place.name])
	return json_response(locations)


def json_response(data):
  return Response(response=json.dumps(data), status=200, mimetype="application/json")


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=4000)
