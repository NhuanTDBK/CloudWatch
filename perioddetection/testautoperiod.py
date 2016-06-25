
# coding: utf-8

# In[1]:

import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import pandas as pd
from pandas import HDFStore

from scipy import signal
from segmentation import segment, fit

# In[7]:

# store = HDFStore("storeTraffic.h5")
# store


# In[8]:

# workload = np.array(store["raw_conn_train"])
# print(workload.shape)


# In[9]:

raw_data = pd.read_csv("../data/dataset1/19.json_remake")
raw_data.interpolate(inplace=True)
workload = raw_data.points
# workload = workload [144*2:144*3]


# In[10]:

#tinh autocorrelation
# dich ve goc toa do truoc khi chay

variance = workload.var()
n = len(workload)
workload2= workload-workload.mean()
r=np.correlate(np.array(workload2), np.array(workload2),mode = 'full')[-n:]
# assert np.allclose(r, np.array([(workload[:n-k]*workload[-(n-k):]).sum() for k in range(n)]))
result = r/(n*variance)
# result = r/(variance*(np.arange(n, 0, -1)))
plt.plot(np.array(range(0,n)),result)

plt.figure(2)
plt.plot(np.array(range(0,workload2.size)), workload);
plt.show()


# In[11]:

# mien tan so
workload2= workload-workload.mean()
fs = 60*24
f, Pxx_den = signal.periodogram(workload, fs)
# chon nguong 40 %
threshold = 0.4 * np.max(Pxx_den);
index_period_candidate = [i for i in range(1,Pxx_den.size-1) if ((Pxx_den[i] > threshold) and (Pxx_den[i] > Pxx_den[i+1]) and (Pxx_den[i] > Pxx_den[i-1]))]
period_candidate = [f[i] for i in index_period_candidate if (f[i]<(n-1)/fs)]
period_candidate_pxx = [Pxx_den[i] for i in index_period_candidate if (f[i]<(n-1)/fs)]

t = {
    'period': period_candidate,
    'magnitude': period_candidate_pxx
}
period_candidate_point = pd.DataFrame(t)
period_candidate_point = period_candidate_point.nlargest(8,'magnitude')

fig = plt.figure(4)
ax = fig.add_subplot(111)

plt.plot(f, Pxx_den)
plt.scatter(period_candidate_point['period'], period_candidate_point['magnitude'],  c='red')
for i,j in zip(period_candidate_point['period'], period_candidate_point['magnitude']):
    ax.annotate('= %s' %i, xy=(i,j), xytext=(10,0), textcoords='offset points')
    ax.annotate('P' , xy=(i,j))

plt.xlabel('Time')
plt.ylabel('Power')
plt.xlim(0, 14)
plt.show()




# In[12]:

#circular autocorrelation

lag = range(0,n-1)
autocorr = [np.correlate(workload,np.roll(workload,-i))[0] / workload.size for i in lag]
ACF_candidate = [autocorr[int(i*fs)] for i in period_candidate_point['period']]
fig = plt.figure(5)
ax = fig.add_subplot(111)
plt.plot(np.array(range(0,n-1))/(1.0*fs),autocorr)

plt.scatter( period_candidate_point['period'], ACF_candidate, c = 'red')

for i,j in zip(period_candidate_point['period'],ACF_candidate):
    ax.annotate('%s ' %i, xy=(i,j), xytext=(3,0), textcoords='offset points')
    ax.annotate('' , xy=(i,j))
# plt.figure(2)
# dif = np.diff(autocorr,n=2)
# plt.plot(dif)
# plt.xlim(0, 5)
plt.xlabel('Time')
plt.ylabel('Circular ACF')
plt.show()
# plt.show()

final_all_period = []
for period_temp in period_candidate_point['period']:
    startpoint = (int)(period_temp * fs)
    temp = autocorr[startpoint]

    begin_frame = np.max([(startpoint - fs), 0])
    end_frame = np.min([startpoint + fs, len(autocorr)])

    max = np.max(autocorr[begin_frame:end_frame])
    min = np.min(autocorr[begin_frame:end_frame])
    tb =(max+min) / 2
    autocorr_normalize = (np.array(autocorr) - tb) / (max-min)
    max_error = 0.005
    print period_temp
    segments = []
    try:
        segments = segment.topdownsegment(autocorr_normalize[begin_frame:end_frame], fit.regression,
                                                fit.sumsquared_error, max_error)
    except:
        pass
    segment.draw_plot(autocorr_normalize[begin_frame:],"Sliding window with regression")
    plt.scatter( startpoint-begin_frame, autocorr_normalize[startpoint], c = 'red')
    segment.draw_segments(segments)
    print segments
    plt.show()
    if len(segments) < 3:
        continue
    #check xem co la hill ko
    # diem start point la 200 (trong khoang moi 401 diem dang xet)
    # tim doan seg cua diem nay
    # seg_index = 0
    for i in range(0,len(segments)):
        if startpoint-begin_frame < segments[i][2]:
            seg_index = i
            break
    if((seg_index < 2) or (seg_index > len(segments)-2)):
        continue
    dh_trai = (segments[seg_index][3]-segments[seg_index][1]) - (segments[seg_index-1][3]-segments[seg_index-1][1])
    dh_phai = (segments[seg_index+1][3]-segments[seg_index+1][1]) - (segments[seg_index][3]-segments[seg_index][1])

    if ((dh_phai<0) and (dh_trai<0)): # diem nam tren hill tien hanh tim closest peak
        while (segments[seg_index][3]>segments[seg_index][1]):
            #di tu trai sang phai
            # khi nao ma dao ham con duong thi di tu trai sang phai
            seg_index = seg_index+1
            if (seg_index > len(segments)-2):
                break
        while (segments[seg_index][3]<segments[seg_index][1]):
            # khi nao dao ham con am thi di tu phai sang trai
            seg_index = seg_index -1
            if((seg_index < 2)):
                break
        if ((seg_index >= 2) and (seg_index <= len(segments) - 2)):
            final_period = segments[seg_index][2]
            final_all_period.append(final_period+begin_frame)
print final_all_period
#tim duoc segment cua diem

# In[ ]:



