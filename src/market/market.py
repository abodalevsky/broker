__author__ = 'abodalevsky'

import logging
from market.market_proxy import MarketProxy



class Market():
    """
    Class Market is used by trader to request price of shares and recommendations buy or sell shares

    Market uses MarketProxy to optimize access to online sources
    """

    __proxy = MarketProxy()

    def get_share(self, code):
        """
        Uses by trader to get prices for shares

        :param code: code {string} of share see match to name in class Shares
        For now it accept only one share at once, later on may be changed to accept list of shares
        :return: share's price and recommendation. Format is following (example):{
            '2186':{
                'price': 55.640,
                'summary':'sell'
            },
            '8849': {
                'price': 58.450,
                'summary':'neutral'
            }
        }
        """
        logging.info('Request for shares: {0}'. format(code))
        basket = dict()
        basket[code] = self.__proxy.get_share(code)

        return basket
