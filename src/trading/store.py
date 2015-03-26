__author__ = 'abodalevsky'

from mysql.connector import *
from market.config import Config


class Store():
    """
    Encapsulate data storage and receiving from DB
    connection is established during creation class
    """
    def brokers(self, extended=False):
        """
        establishes connection to db and retrieves list of brokers
        :param extended: if set to true returns full info about broker e.g. id, name, rating if set to false
        returns list of id only
        :return: list of brokers
        """
        return self.__brokers_full() if extended else self.__brokers_id()

    def __brokers_id(self):
        q = "SELECT idbrocker FROM brocker"
        l = list()
        with DbCursor() as cursor:
            cursor.execute(q)
            for row in cursor:
                id, = row
                l.append(id)

        return l

    def __brokers_full(self):
        q = "SELECT * FROM brocker"
        l = list()
        with DbCursor() as cursor:
            cursor.execute(q)
            for row in cursor:
                id, name, rating = row
                broker = {
                    'idbrocker': int(id),
                    'name': str(name),
                    'rating': int(rating)
                }
                l.append(broker)

        return l

    def all_clients(self):
        """
        :return: list of all clients that are registered in DB in format: [{
            'idclient': 1,
            'broker': 'Broker Name',
            'name': 'Client Name',
            'balance': 123.55
        }]
        """
        q = """SELECT clients.idclients, brocker.name, clients.name, clients.balance
                FROM clients
                INNER JOIN brocker
                ON clients.idbrocker=brocker.idbrocker"""
        l = list()
        with DbCursor() as cursor:
            cursor.execute(q)
            for idclient, broker, name, balance in cursor:
                client = {
                    'idclient': int(idclient),
                    'broker': str(broker),
                    'name': str(name),
                    'balance': float(balance)
                }
                l.append(client)
        return l

    def clients(self, broker):
        """
        establishes connection to db and retrieves list of clients
        :param broker: id of broker where clients are searched for
        :return: list of clients in format:{
            'idclients':123,
            'name': 'CoolClient',
            'balance': 1056.33
        }
        """
        q = ("SELECT idclients, name, balance FROM clients WHERE idbrocker= %s")
        l = list()
        with DbCursor() as cursor:
            cursor.execute(q, (broker,))
            for id, name, balance in cursor:
                client = {
                    'idclients': int(id),
                    'name': str(name),
                    'balance': float(balance)
                }
                l.append(client)

        return l

    def client(self, client):
        """

        :param client: id of client
        :return: full info about the client in format: {
            'name': 'CoolClient',
            'balance': 1056.33
        }
        """
        q = ("SELECT name, balance FROM clients WHERE idclients= %s")
        with DbCursor() as cursor:
            cursor.execute(q, (client,))
            try:
                data = cursor.next()
                client = {
                    'name': str(data[0]),
                    'balance': float(data[1])
                }
            except StopIteration:
                client = {}
        return client

    def actives(self, client):
        """
        returns list of actives for given client
        :param client: client's ID
        :return: list of actives in format:{
            'idactives': 1
            'name': 8899,
            'quantity': 125365
        },
        """

        q = ("SELECT idactives, name, quantity FROM actives WHERE idclient= %s")
        l = list()
        with DbCursor() as cursor:
            cursor.execute(q, (client,))
            for id, name, quantity in cursor:
                client = {
                    'idactives': int(id),
                    'code': str(name),
                    'quantity': int(quantity)
                }
                l.append(client)

        return l

    def update_active(self, code, quantity):
        """
        update number of shares for given code
        :param code: code of shares that will be updated
        :param code: new number of shares
        :return: nothing
        """
        q = ("UPDATE actives SET quantity='%s' WHERE idactives='%s'")
        with DbCursor(False) as cursor:
            cursor.execute(q, (quantity, code))

    def update_balance(self, client, new_balance):
        """
        updates balance for given client
        :param client: ID of the client
        :param new_balance: new amount of money
        :return:
        """
        q = ("UPDATE clients SET balance='%s' WHERE idclients='%s'")
        with DbCursor(False) as cursor:
            cursor.execute(q, (new_balance, client))


class DbCursor():
    """
    will encapsulate creation connection and freeing resources,
    must be used via with statement
    """
    __read_only = True

    __config = {
        'user': 'super',
        'database': 'brocker',
        'host': '0.0.0.0',
        'password': '12345:)'
    }

    def __init__(self, read_only=True):
        self.__read_only = read_only
        self.__config['host'] = Config.STORAGE_HOST

    def __enter__(self):
        # TODO: check exceptions!!!
        self.__connection = connect(**self.__config)
        self.__cursor = self.__connection.cursor()
        return self.__cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.__read_only:
            self.__connection.commit()  # TODO: commit should be performed if no exceptions were risen!
        self.__cursor.close()
        self.__connection.close()