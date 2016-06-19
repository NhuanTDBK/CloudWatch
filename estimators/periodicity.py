
# coding: utf-8

# In[1]:

from scipy import signal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from io_utils.GFeeder import GFeeder

# In[9]:
# dataFeeder = GFeeder(split_size=5)
# raw_data = dataFeeder.read()
# n_row = raw_data.shape[0]
# workload = raw_data[dataFeeder.CPU_UTIL]
#workload = pd.read_json('../data/gdata/metric_778700158_1min.json',orient='records')["cpu"]


# In[10]:
def estimate_period(workload,period=144.0):
    #tinh autocorrelation
    # dich ve goc toa do truoc khi chay
    n = len(workload)
    variance = workload.var()
    workload2= workload-workload.mean()
    r=np.correlate(workload2, workload2,mode = 'full')[-n:]
    # assert np.allclose(r, np.array([(workload[:n-k]*workload[-(n-k):]).sum() for k in range(n)]))
    result = r/(n*variance)
    # result = r/(variance*(np.arange(n, 0, -1)))
    plt.plot(np.array(range(0,n))/period,result)

    plt.figure(2)
    plt.plot(np.array(range(0,workload2.size))/period, workload);
    plt.show()


    # In[11]:

    # mien tan so
    workload2= workload-workload.mean()
    fs = 6*24
    f, Pxx_den = signal.periodogram(workload, fs)
    # chon nguong 40 %
    threshold = 0.4 * np.max(Pxx_den);
    index_period_candidate = [i for i in range(1,Pxx_den.size-1) if ((Pxx_den[i] > threshold) and (Pxx_den[i] > Pxx_den[i+1]) and (Pxx_den[i] > Pxx_den[i-1]))]
    period_candidate = [f[i] for i in index_period_candidate]
    period_candidate_pxx = [Pxx_den[i] for i in index_period_candidate]

    fig = plt.figure(4)
    ax = fig.add_subplot(111)

    plt.plot(f, Pxx_den)
    plt.scatter(period_candidate, period_candidate_pxx,  c='red')
    for i,j in zip(period_candidate,period_candidate_pxx):
        ax.annotate('= %s' %i, xy=(i,j), xytext=(10,0), textcoords='offset points')
        ax.annotate('P' , xy=(i,j))

    plt.xlabel('Time')
    plt.ylabel('Power')
    plt.xlim(0, 14)
    plt.show()

    # In[12]:

    #circular autocorrelation

    lag = range(1,int(period)*5)
    autocorr = [np.correlate(workload,np.roll(workload,-i))[0] / workload.size for i in lag]
    ACF_candidate = [autocorr[int(i*period)] for i in period_candidate]
    fig = plt.figure(5)
    ax = fig.add_subplot(111)
    plt.plot(np.array(range(1,int(period)*5))/period,autocorr)
    plt.scatter(period_candidate, ACF_candidate, c = 'red')
    for i,j in zip(period_candidate,ACF_candidate):
        ax.annotate('%s day' %i, xy=(i,j), xytext=(3,0), textcoords='offset points')
        ax.annotate('' , xy=(i,j))
    # plt.figure(2)
    # dif = np.diff(autocorr,n=2)
    # plt.plot(dif)
    plt.xlim(0, 5)
    plt.xlabel('Time')
    plt.ylabel('Circular ACF')

    plt.show()


# In[ ]:



