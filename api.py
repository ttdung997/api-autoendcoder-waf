from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask import jsonify
from lib.http_detection import HttpPredict
import threading
import time
import base64



# check_token =("SELECT COUNT(1) FROM bkcs_oauth_token WHERE token = %(token)s ") 

app = Flask(__name__)
api = Api(app)

model = HttpPredict()
model.loadModelInit()


class TestApi(Resource):
	def get(self):
	  	return 0

class PredictApi(Resource):
	def get(self, input_str):
		try:
			input_str += "=" * ((4 - len(input_str) % 4) % 4) 
			data = base64.b64decode(str(input_str)).decode("utf-8")
		except:
			return 0
		if data is None:
			return "0"
		prepareData = model.preprocess(data)
		if prepareData is None:
			return "0"

		result = model.predict(prepareData)
		if result is None:
			return "0"
		return (result)
		if result < 0.5 :
			return "0"
		return "1"


api.add_resource(TestApi, '/test/')
api.add_resource(PredictApi, '/<input_str>') # Route_1


if __name__ == '__main__':
	domain = 'POST /12324asdsad'
	prepareData = model.preprocess(domain)
	print(prepareData)
	result = model.predict(prepareData)
	print(result)

	app.run(host='localhost',port='5003')
	 
