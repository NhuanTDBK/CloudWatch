from outlier.BaseOutlier import BaseOutlier
from sklearn.svm import OneClassSVM
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

class KMeansBase(BaseOutlier):
    @staticmethod
    def get_attributes():
        return {
            "nu":0.1,
            "kernel":['rbf','linear', 'poly', 'rbf', 'sigmoid', 'precomputed'],
            "gamma":0.1,
        }
    def __init__(self,nu=0.1,kernel='rbf',gamma=0.1, window_size = 32, n_cluster = 150, error_thres = 0.05):
        self.nu = nu
        self.kernel = kernel
        self.gamma = gamma
        self.window_size = window_size
        self.n_cluster = n_cluster
        self.error_thres = error_thres
    def sliding_chunker(self,data, window_len, slide_len):
        """
        Split a list into a series of sub-lists, each sub-list window_len long,
        sliding along by slide_len each time. If the list doesn't have enough
        elements for the final sub-list to be window_len long, the remaining data
        will be dropped.

        e.g. sliding_chunker(range(6), window_len=3, slide_len=2)
        gives [ [0, 1, 2], [2, 3, 4] ]
        """
        chunks = []
        for pos in range(0, len(data), slide_len):
            chunk = np.copy(data[pos:pos + window_len])
            if len(chunk) != window_len:
                continue
            chunks.append(chunk)

        return chunks

    def plot_waves(self,waves, step):
        """
        Plot a set of 9 waves from the given set, starting from the first one
        and increasing in index by 'step' for each subsequent graph
        """
        plt.figure()
        n_graph_rows = 3
        n_graph_cols = 3
        graph_n = 1
        wave_n = 0
        for _ in range(n_graph_rows):
            for _ in range(n_graph_cols):
                axes = plt.subplot(n_graph_rows, n_graph_cols, graph_n)
                axes.set_ylim([-100, 150])
                plt.plot(waves[wave_n])
                graph_n += 1
                wave_n += step
        # fix subplot sizes so that everything fits
        plt.tight_layout()
        plt.show()

    def reconstruct(self,data, window, clusterer):
        """
        Reconstruct the given data using the cluster centers from the given
        clusterer.
        """
        window_len = len(window)
        slide_len = window_len / 2
        segments = self.sliding_chunker(data, window_len, slide_len)
        reconstructed_data = np.zeros(len(data))
        for segment_n, segment in enumerate(segments):
            # window the segment so that we can find it in our clusters which were
            # formed from windowed data
            segment *= window
            nearest_match_idx = clusterer.predict(segment)[0]
            nearest_match = np.copy(clusterer.cluster_centers_[nearest_match_idx])

            pos = segment_n * slide_len
            reconstructed_data[pos:pos + window_len] += nearest_match

        return reconstructed_data

    def get_windowed_segments(self,data, window):
        """
        Populate a list of all segments seen in the input data.  Apply a window to
        each segment so that they can be added together even if slightly
        overlapping, enabling later reconstruction.
        """
        step = 2
        windowed_segments = []
        # print len(window)
        segments = self.sliding_chunker(data, window_len = len(window), slide_len=step)
        for segment in segments:
            segment *= window
            windowed_segments.append(segment)
        return windowed_segments

    def fit(self,data=None):
        self.data = data
        self.check_finite(data)
        if(self._is_using_pandas(data)==True):
            self.data.interpolate(inplace=True)
        return self
    def predict(self, data):
        dat = np.array(data)
        window_rads = np.linspace(0, np.pi, self.window_size)
        window = np.sin(window_rads) ** 2
        # print("Windowing data...")
        windowed_segments = self.get_windowed_segments(dat, window)
        # print("Clustering...")
        clusterer = KMeans(n_clusters=self.n_cluster)
        clusterer.fit(windowed_segments)
        reconstruction = self.reconstruct(dat, window, clusterer)
        error = reconstruction - dat
        threshold = (np.max(dat) - np.min(dat)) * self.error_thres
        outlier_idx = [i for i in range(0, len(error)) if error[i] > threshold]
        d = {
            'timestamp': self.data.index[outlier_idx],
            'anoms': self.data.iloc[outlier_idx]
        }
        anoms = pd.DataFrame(d)
        self.anomaly_idx = anoms.index
        self.anom_val = anoms['anoms']
        return anoms
    def fit_predict(self, data=None):
        self.fit(data)
        return self.predict(data)
    def plot(self):
        import matplotlib.pyplot as plt
        f, ax = plt.subplots(1, 1)
        ax.plot(self.data, 'b')
        ax.plot(self.anomaly_idx, self.anom_val, 'ro')
        ax.set_title('Detected Anomalies')
        ax.set_ylabel('Count')
        f.tight_layout()
        return f
