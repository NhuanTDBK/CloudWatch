from influxdb import DataFrameClient
class DataSource(object):
    def __init__(self,host="localhost",port='8086',username="root",password="root",db_name=None,measurement=None):

        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db_name = db_name
        self.measurement = measurement

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