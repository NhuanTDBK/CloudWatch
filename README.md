# CloudWatch
Automatic Anomaly Detection with minimal setup

How to setup
--------
-  Run `bash install_bashrc` to install package dependencies
-  Run configuration InfluxDB on config.cfg
-  Run configuration Grafana on Setup_Influxdb_and_Grafana to visualize anomaly detections

How to use
---------
- Change number of updates (seconds) and time to detect (second) on config.cfg
- Run simulate data follow by command `ipython simulate_data/SimulateStream.py "data_path" & ` with `data_path` is data directory
- Run service: `ipython experiments/TestService.py &`

Web app UI
---------
- Run app.py and access to localhost:5000 
