import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
import seaborn as sb
#
dat = pd.read_csv('../data/vc_1.csv',index_col=0,parse_dates=True)
decomfreq = 24 * 60
res = sm.tsa.seasonal_decompose(dat.points.interpolate().tolist(),freq=decomfreq, model='addtitive')
res.plot()
# centrumGalerie = pd.read_csv('../data/Centrum-Galerie-Belegung.csv',
#  names=['Datum', 'Belegung'],
#  index_col=['Datum'],
#  parse_dates=True)
# decompfreq = 24*60/15*7
# res = sm.tsa.seasonal_decompose(centrumGalerie.Belegung.interpolate(),
# freq=decompfreq,
# model='additive')