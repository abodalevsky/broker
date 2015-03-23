__author__ = 'abodalevsky'

import logging


class Shares():
    """ Encapsulate knowledge about shares
    """

    __SHARES = {
        1:        {'name': 'EUR-USD',   'for_exchange': 5,    'active_for_exchange': 15,    'usd': True},
        2:        {'name': 'GPB-USD',   'for_exchange': 2,    'active_for_exchange': 8,     'usd': True},
        3:        {'name': 'USD-JPU',   'for_exchange': 500,  'active_for_exchange': 700,   'usd': False},
        2186:     {'name': 'USD-RUB',   'for_exchange': 1000, 'active_for_exchange': 10000, 'usd': False},
        8830:     {'name': 'GOLD',      'for_exchange': 1,    'active_for_exchange': 4,     'usd': True},
        8836:     {'name': 'SILVER',    'for_exchange': 10,   'active_for_exchange': 15,    'usd': True},
        8833:     {'name': 'OIL_BRENT', 'for_exchange': 20,   'active_for_exchange': 50,    'usd': True},
        8849:     {'name': 'OIL_WTI',   'for_exchange': 20,   'active_for_exchange': 50,    'usd': True},
        8883:     {'name': 'PALLAD',    'for_exchange': 2,    'active_for_exchange': 5,     'usd': True},
        8831:     {'name': 'CUPRUM',    'for_exchange': 200,  'active_for_exchange': 600,   'usd': True},
        8910:     {'name': 'PLATINUM',  'for_exchange': 1,    'active_for_exchange': 3,     'usd': True},
        13665:    {'name': 'RTS',       'for_exchange': 1,    'active_for_exchange': 4,     'usd': True},
        13666:    {'name': 'MMVB',      'for_exchange': 1,    'active_for_exchange': 4,     'usd': True},
        172:      {'name': 'DAX',       'for_exchange': 1,    'active_for_exchange': 2,     'usd': True},
        27:       {'name': 'FTSE100',   'for_exchange': 1,    'active_for_exchange': 3,     'usd': True}
    }

    def get_details(self, code):
        """
        :param code: code of share {int}
        :return: return its text representation
        """
        try:
            return self.__SHARES[int(code)]
        except (KeyError, ValueError):
            err = 'Invalid code: {0}'.format(code)
            logging.error(err)
            return err

    def get_price_in_usd(self, code, price):
        """
        :param code: code of share
        :param price: price received from market
        :return: price in USD. In case of invalid code - it rises Exception (KeyError)
        """
        return price if self.__SHARES[int(code)]['usd'] else float(1/price)
