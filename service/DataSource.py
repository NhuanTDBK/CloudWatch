from influxdb import DataFrameClient
class DataSource(object):
    def __init__(self,host="localhost",port='8086',username="root",password="root",db_name=None,measurement=None):

        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db_name = db_name
        self.measurement = measurement
        if self._check_influxdb_connected(host, port, username, password, db_name):
            self.client_api = DataFrameClient(host, port, username, password, db_name)

    def _check_influxdb_connected(self, host, port, username, password, db_name):
        client = DataFrameClient(host, port, username, password, db_name)
        result = True
        try:
            client.get_list_database()
            print "Connect to database server"
        except:
            result = False
            print "Cannot connect. Please check configuration server"
        return result
    def check_connected(self):
        return self._check_influxdb_connected(self.host,self.port,self.username,self.password,self.db_name)
    def _return(self):
        return self.host,self.port,self.username,self.password,self.db_name,self.measurement

    def query_analyzed(self, number_of_days =30):
        print "Get latest time series points"
        query_set = 'select value from %s order by time desc limit %s ;' % (
        self.measurement, number_of_days * 24 * 60)
        result = self.client_api.query(query_set)[self.measurement]
        return result
    def query_all(self):
        print "Get latest time series points"
        query_set = 'select value from %s limit 10000;' % (self.measurement)
        result = self.client_api.query(query_set)[self.measurement]
        return result
    def update_db(self,data):
        result = False
        try:
            result = self.client_api.write_points(data,self.measurement)
        except Exception as e:
            print e.message
        return result