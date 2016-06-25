# **Hướng dẫn cài đặt Influxdb và Grafana**
  Trong nội dung project này, chúng tôi sử dụng Influxdb database để lưu trữ dữ liệu và Grafana để hiển thị dữ liệu cũng như các *điểm bất thường*

  Để tiện lợi và đảm bảo cho việc người dùng dễ dàng cài đặt, chúng tôi đề xuất sử dụng Docker container kết hợp cả Influxdb và Grafana. Hiện tại có rất nhiều docker images được chia sẻ miễn phí trên Docker Hub. Ở đây, chúng tôi sử dụng docker images [samuelebistoletti/docker-statsd-influxdb-grafana
](https://github.com/samuelebistoletti/docker-statsd-influxdb-grafana). Tìm hiểu thêm về Docker tại [https://www.docker.com/](https://www.docker.com/)

  Khi đã có docker image trên, chúng ta đơn giản là thực hiện lệnh theo đường dẫn image ở trên:

  docker run -d \
  --name docker-statsd-influxdb-grafana \
  -p 3003:9000 \
  -p 3004:8083 \
  -p 8086:8086 \
  -p 22022:22 \
  -p 8125:8125/udp \
  samuelebistoletti/docker-statsd-influxdb-grafana

# **Hướng dẫn cấu hình**

  Sau khi container của docker đã chạy. Chúng ta thực hiện cấu hình địa chỉ của database cho project này và Grafana để hiển thị dữ liệu.

  1. Truy cập [http://localhost:3003](http://localhost:3003)

    Username: root
    Password: root

  2. Vào mục Data Sources -> Add new :

    Url: http://localhost:8086
    
    Type: InfluxDB 0.9.x
    
    Access: Direct
    
    Database: test
    
    User: datasource
    
    Password: datasource

    Thực hiện *Test connection* và *Save*

  3. Quay lại Dashboard -> Home -> New (góc dưới trái).

    Tiếp tục click chuột vào phần xanh lá cây lề trái -> Add Panel -> Graph

    Sau đó, thực hiện chọn datasource mà bạn đã tạo ở góc dưới phải.

    Tiếp tục tạo hai câu truy vấn như sau:

    A: SELECT "value" FROM "data"
    
    B: SELECT "value" FROM "data" WHERE "anomaly" = 0

    Chuyển tới *Display Styles* và thêm hai *Series specific overrides * như sau:

    alias or regex : normal  Lines: true   Points: false
    
    alias or regex : anomaly Lines: false  Points: true

  4. Trong quá trình theo dõi dữ liệu được đẩy liên tục vào database, để tiện theo dõi, chúng ta có thể thay đổi khoảng thời gian quan tâm cũng như tấn suất cập nhật đồ thị bằng thao tác ngay trên giao diện.
