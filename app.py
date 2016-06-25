from flask import Flask, jsonify, abort, request, make_response, url_for
from service.BaseEngine import BaseEngine
from utils.auto_load import AutoLoad
from service.DataSource import DataSource
from service_form.ServiceForm import *


loader = AutoLoad()
app = Flask(__name__)
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', '*')
  response.headers.add('Access-Control-Allow-Methods', '*')
  return response


@app.route("/")
def hello():
    return "Hello World!"
@app.route('/algorithm/<algo>/params')
def getParams(algo):
    obj = loader.load_engine(algo)
    params = obj.get_attributes()
    return jsonify(params)
@app.route('/create', methods = ['POST'])
def api_predict():
    if request.method == "POST":
        params_form = parse(request.form)
        # obj = loader.load_engine()
        engine = loader.auto_constructor(params_form['submit_algo'],params_form)
        datasource = DataSource(host=params_form['host'], port=params_form['port'], username=params_form['user-name'],
                            password=params_form['password'],db_name=params_form['db_name'],measurement=params_form['measurement'])
        service = BaseEngine(engine=engine,datasource=datasource)
        #
        return jsonify(request.form)
if __name__ == "__main__":
    app.run()