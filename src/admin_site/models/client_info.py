__author__ = 'abodalevsky'
import logging
from trading.store import Store
from market.shares import Shares


class ClientInfo:
    """ Prepares full information about client


    """
    def get_full_info(self, client_id):
        """

        :param client_id: id of the client
        :return: dictionary with full info about client and actives in format: {
            'name': 'Test Cli',
            'balance': 12345.67,
            'actives': [
                {
                    'idactives': 1,
                    'code': 3,
                    'quantity': 150,
                    'details': {
                      'name': 'USD-JPU',
                      'for_exchange': 500,
                      'active_for_exchange': 700,
                      'usd': False
                    }
                },
                ....
            ]
        }
        """

        storage = Store()
        client = storage.client(client_id)
        if client == {}:
            logging.error('No client with id:{0}'.format(client_id))
            return client

        actives = storage.actives(client_id)
        shares = Shares()
        for active in actives:
            active['details'] = shares.get_details(active['code'])

        client['actives'] = actives

        return client