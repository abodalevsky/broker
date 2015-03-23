__author__ = 'abodalevsky'

import logging
from market.adapters import response_to_values
from market.connector import get_shares


class Market():
    """Class Market is used by trader to request price of shares and recommendations buy or sell shares

        Market uses MarketProxy to optimize access to online sources
    """

    def get_share(self, code):
        """Uses by trader to get prices for shares

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
        shares = response_to_values(get_shares(code))
        for share, value in shares.items():
            logging.info('Received share for {0}'.format(share))
            basket[share.strip()] = self.__add_to_basket(value['summaryLast'], value['technicalSummaryClass'])

        return basket

    def __add_to_basket(self, price, summary):
        try:
            pr = round(float(price.replace(',', '.')), 3)
        except ValueError as e:
            logging.error('Wrong format: ' + repr(e))
            pr = 0

        logging.info('\t price: {0}, summary: {1}'.format(pr, summary))
        return {'price': pr, 'summary': summary}

