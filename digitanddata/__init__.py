import pymysql

# Shared hosting (GoDaddy) can't compile the mysqlclient C extension, so the
# project uses the pure-Python PyMySQL driver and registers it under the
# MySQLdb name Django's mysql backend expects.
pymysql.install_as_MySQLdb()
