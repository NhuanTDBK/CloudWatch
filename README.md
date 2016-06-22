# CloudWatch
Hệ thống phát hiện và tự động cảnh báo bất thường trong hệ thống
# Cách dùng engine:
Đọc trực tiếp từ file (xem file experiments/TestEngine.py):
    engine = loader.auto_load_engine_default(method='SHESD')
    dat = pd.read_csv('../data/vc_1.json_remake',index_col=0,parse_dates=True)
    engine.fit_predict(data=dat.points)
    engine.plot()
Sử dụng service lấy dữ liệu từ Influxdb
    engine = loader.auto_load_engine_default(method='SHESD')
    # Cau hinh lai db name va measurement tro toi CSDL Influxdb
    # Service tu dong load 20 ngay gan nhat de du doan anomaly
    service = BaseEngine(engine=engine,db_name='example',measurement='vc1_2weeks', number_of_days=20)