# CloudWatch
Hệ thống phát hiện và tự động cảnh báo bất thường trong hệ thống
dashboard 
/home/nhuanhunter/MyWorking/CloudWatch/gentelella/production/dashboard.html
# Cách dùng engine:
chạy giả lập dữ liệu real time
 ipython simulate_data/SimulateStream.py "data_path" & với data_path là đường dẫn tới dữ liệu
chạy service phát hiện bất thường
 ipython experiments/TestService.py &
