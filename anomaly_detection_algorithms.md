# **Các thuật toán được sử dụng trong engine**
  1. Thuật toán sử dụng cho seasonal time series (dữ liệu có chu kỳ): outlier/SHESD.py, outlier/STL.py
    - Bước 1: Phát hiện và đánh giá chu kỳ sử dụng phương pháp AUTOPERIOD (periodetection/autoperiod.py) xem thêm về thuật toán này trong  [On Periodicity Detection and Structural Periodic Similarity](http://alumni.cs.ucr.edu/~mvlachos/pubs/sdm05.pdf)
    - Bước 2: Chu kỳ tìm được trong bước 1 được sử dụng để phân tích time series thành các thành phần: Trend, Seasonal và residual.
            Một số kỹ thuật được sử dụng: moving average, moving median, sliding window
    - Bước 3: Sử dụng thành phần residual để phát hiện điểm bất thường, thuật toán được sử dụng: 
         + Anomaly detection with the normal distribution
         + Extreme Studentized Deviate (ESD)
         + Anomaly Detection with Poisson Distribution
  2. Thuật toán cho time series không có chu kỳ: phương pháp AUTOPERIOD giúp xác định time series có chy kỳ hay không. Khi dữ liệu không có chu kỳ, các thuật toán sau được sử dụng:
    - OneClassSVM: dựa trên Support vector machine
    - KMeans: dựa trên phương pháp phân cụm K-means 
    - các thuật toán trong Bước 3 của phần 1