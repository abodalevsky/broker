# broker old

todo: Add DB connection problem handling
Traceback (most recent call last):
  File "/usr/local/lib/python3.4/site-packages/mysql/connector/network.py", line 467, in open_connection
    self.sock.connect(sockaddr)
ConnectionRefusedError: [Errno 111] Connection refused

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "./runner.py", line 49, in <module>
    run()
  File "./runner.py", line 41, in run
    t.trade()
  File "/usr/src/app/trading/trader.py", line 79, in trade
    for broker in self.get_brokers_id():
  File "/usr/src/app/trading/trader.py", line 41, in get_brokers_id
    return self.__store.brokers()
  File "/usr/src/app/trading/store.py", line 19, in brokers
    return self.__brokers_full() if extended else self.__brokers_id()
  File "/usr/src/app/trading/store.py", line 24, in __brokers_id
    with DbCursor() as cursor:
  File "/usr/src/app/trading/store.py", line 192, in __enter__
    self.__connection = connect(**self.__config)
  File "/usr/local/lib/python3.4/site-packages/mysql/connector/__init__.py", line 159, in connect
    return MySQLConnection(*args, **kwargs)
  File "/usr/local/lib/python3.4/site-packages/mysql/connector/connection.py", line 129, in __init__
    self.connect(**kwargs)
  File "/usr/local/lib/python3.4/site-packages/mysql/connector/connection.py", line 454, in connect
    self._open_connection()
  File "/usr/local/lib/python3.4/site-packages/mysql/connector/connection.py", line 417, in _open_connection
    self._socket.open_connection()
  File "/usr/local/lib/python3.4/site-packages/mysql/connector/network.py", line 470, in open_connection
    errno=2003, values=(self.get_address(), _strioerror(err)))
mysql.connector.errors.InterfaceError: 2003: Can't connect to MySQL server on '172.23.74.110:3306' (111 Connection refused)

