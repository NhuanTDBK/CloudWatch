import pandas as pd
import numpy as np
import json
import os

print os.getcwd()
folder_name = 'data/dataset1'
columns = ["points","timestamp"]
for name in os.listdir('data/dataset1'):
        if (name.endswith(".json")):
                filename = "%s/%s"%(folder_name,name)
                dat = json.load(open(filename,'rb'))[0]
                df = pd.DataFrame(dat["datapoints"],columns=columns)
                timeindex = pd.to_datetime(df.timestamp,unit='s')
                df = df.set_index(timeindex)
                df.to_csv('%s_remake'%filename)


