__author__ = 'abodalevsky'

import logging
from http.client import HTTPConnection
from market.config import Config


def get_shares(shares):
    """Connects to market and get requested shares in JSON format

   :param shares: string with list of shares '1, 25, 45'  meaning can be seen in market.Config
   :return: received json (dictionary), if data retrieving failed - empty dict will be returned
    """
    try:
        logging.debug('connector: init connection')
        conn = HTTPConnection(Config.url())
        conn.request('GET', Config.request(shares, 5), headers=Config.header())

        response = conn.getresponse()
        status = response.status

        if status != 200:
            logging.warning('Connection status is invalid ({0})'.format(status))
            return

        return response.read()

    except Exception as ex:
        logging.error('HTTP error occurred during connection. Reason: ' + repr(ex))
        return
