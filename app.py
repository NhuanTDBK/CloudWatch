from flask import Flask, jsonify, abort, request, make_response, url_for, render_template
from service.BaseEngine import BaseEngine
from utils.auto_load import AutoLoad
from service.DataSource import DataSource
from service_form.ServiceForm import *
import uuid
import numpy as np
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import sys
from perioddetection import autoperiod

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

loader = AutoLoad()
app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()
services = {}

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', '*')
  response.headers.add('Access-Control-Allow-Methods', '*')
  return response
@app.route("/")
def hello():
    return render_template('dashboard.html')
@app.route("/check_db", methods=["POST"])
def check_db():
    if request.method == "POST":
        params = request.form

        new_params = {}
        new_params['host'] = str(params['host'])
        new_params['user-name'] = str(params['user-name'])
        new_params['password'] = str(params['password'])
        new_params['db_name'] = str(params['db_name'])
        new_params['measurement'] = str(params['measurement'])
        params_form = new_params
        datasource = DataSource(host=params_form['host'], username=params_form['user-name'],
                                password=params_form['password'], db_name=params_form['db_name'],
                                measurement=params_form['measurement'])
        result = {"status":"failed"}
        if datasource.check_connected() == True:
            result['status'] = "good"
        # else:
            # result = "failed"
        return jsonify(result=result)
@app.route('/service')
def index_table():
    return render_template('index2.html')
@app.route('/algorithm/<algo>/params')
def getParams(algo):
    obj = loader.load_engine(algo)
    params = obj.get_attributes()
    return jsonify(params)
@app.route('/check_running')
def check_running():
    # obj = loader.load_engine(algo)
    number_of_services = len(services)
    # params = obj.get_attributes()
    return jsonify(number_of_services=number_of_services)
@app.route('/create', methods = ['POST'])
def api_predict():
    if request.method == "POST":
        params_form = parse(request.form)
        # obj = loader.load_engine()
        engine = loader.auto_constructor(params_form['submit_algo'],params_form)
        datasource = DataSource(host=params_form['host'], port=params_form['port'], username=params_form['user-name'],
                            password=params_form['password'],db_name=params_form['db_name'],measurement=params_form['measurement'])
        service = BaseEngine(engine=engine,datasource=datasource)
        id_service = str(uuid.uuid4())
        services[id_service] = service
        try:
            scheduler.add_job(services[id_service].work, 'interval', seconds=30, id=id_service)
        except Exception as e:
            print e
        #
        return jsonify(request.form)
@app.route('/check_period', methods = ['POST'])
def period_detect():
    if request.method == "POST":
        params = request.form
        new_params = dict(request.form)
        new_params['host'] = str(params['host'])
        new_params['user-name'] = str(params['user-name'])
        new_params['password'] = str(params['password'])
        new_params['db_name'] = str(params['db_name'])
        new_params['measurement'] = str(params['measurement'])
        new_params['port'] = int(params['port'])
        params_form = new_params
        datasource = DataSource(host=params_form['host'], port=params_form['port'], username=params_form['user-name'],
                                password=params_form['password'], db_name=params_form['db_name'],
                                measurement=params_form['measurement'])
        engine = loader.auto_load_engine_default(method='SHESD')
        # service = BaseEngine(engine=engine, datasource=datasource)
        a = engine.convert_twitter_format(datasource.query_all().value)
        return jsonify(periods=autoperiod.period_detect(a, segment_method="topdownsegment"))
if __name__ == "__main__":
    app.run()