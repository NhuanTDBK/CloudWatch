# CloudWatch
Hệ thống phát hiện và tự động cảnh báo bất thường trong hệ thống
dashboard 

Hướng dẫn cài đặt
--------
-  Chạy file bash install_bashrc để cài đặt các gói phần mềm
-  Thiết lập cấu hình InfluxDB trong file config.cfg
-  Thiết lập cấu hình Grafana trong file Setup_Influxdb_and_Grafana để visuzalize các bất thường

Sử dụng
---------
- Cấu hình thời gian (theo giây) real time dữ liệu (time_of_input_points) và thời gian phát hiện bất thường (time_of_detect) trong file config.cfg
- chạy giả lập dữ liệu real time ipython simulate_data/SimulateStream.py "data_path" & với data_path là đường dẫn tới dữ liệu ( file dữ liệu định dạng json_remake được lưu ở thư mục data)
- chạy service phát hiện bất thường ipython experiments/TestService.py &


Phiên bản web
---------
- Chạy file app.py, truy cập vào đường dẫn localhost:5000 để khởi tạo 1 dịch vụ phát hiện bất thường
