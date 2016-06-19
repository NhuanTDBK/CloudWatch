from pandas import read_json
import numpy as np

path = '../data/gdata/metric_778700158.json'
dat = read_json(path,orient='records')
