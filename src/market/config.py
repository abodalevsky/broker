__author__ = 'abodalevsky'

import sys
import logging
import time
import urllib.parse


"""Share name and its code

"""

RECOMMENDATION = {'AS', 'S', 'N', 'B', 'AB'}


class Config():
    """Class knows all technical details connection to the market

    Data will be hardcoded, later on may be redesigned for INI file or database
    """

    """
    Static variables for storage
    """
    STORAGE_HOST = '0.0.0.0'
    STORAGE_USER = 'super'
    STORAGE_PASSWORD = '12345:)'
    STORAGE_DATABASE_NAME = 'brocker'

    __HOST_FLAG = '-storage_host:'

    """
    Values for logging
    """
    LOG_LEVEL = logging.NOTSET
    __LOG_FLAG = '-log:'

    @staticmethod
    def init(*args):
        """
        Analyse:
            - ini file and initialize with given settings (not implemented yet)
            - command line, overwrite settings, if any
        :param args: list of arguments
        :return: None
        """
        logging.info('Fetch data from command line')

        for arg in args[1:]:
            logging.debug('\t\tparse: {0}'.format(arg))
            if arg.startswith(Config.__HOST_FLAG):
                Config.STORAGE_HOST = arg.lstrip(Config.__HOST_FLAG)
                logging.info('\t\tstorage host: {0}'.format(Config.STORAGE_HOST))
            elif arg.startswith(Config.__LOG_FLAG):
                Config.LOG_LEVEL = int(arg.lstrip(Config.__LOG_FLAG))
                logging.info('\t\tstorage host: {0}'.format(Config.LOG_LEVEL))
            else:
                logging.info('\t\t!!! unrecognized parameter!!!')

    @staticmethod
    def url():
        return 'ru.investing.com'

    @staticmethod
    def request(tsb, pulse=5):
        """formats request to market
        :param tsb: string with shares codes separated by comma ('1, 124, 568')
        :param pulse: should be aliquot to 5 in order to return correct response
        :return: ready to send GET request
        """
        tsb_quoted = urllib.parse.quote(tsb)
        t = int(time.time())
        return '/common/refresher_new/refresher_v13.2.php?\
pulse={0}&\
refresher_version=v1.7.0&\
session_uniq_id=a9cf90ed6a67dfe4be41c6f7dc496daf&\
sideblock_recent_quotes=0&\
sideblock_quotes_exists=0&\
quotes_bar_exists=0&\
economicCalendar_exists=0&\
markets_page_exists=0&\
technical_summary_box_exists=1&\
smlID=103260&\
fpcharts%5B%5D=%5B%5D&\
fpcharts%5B%5D=%5B%5D&\
sideblock_quotes_selected=QBS_3&\
quotes_bar_selected=0&\
PortfolioSideBoxTime={1}&\
RQSideBoxTime={1}&\
MyPortfolioTime={1}&\
tsb_activePairs={2}&\
tsb_currentTimeframe=60'.format(pulse, t, tsb_quoted)

    @staticmethod
    def header():
        return {
            'Host': 'ru.investing.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:34.0) Gecko/20100101 Firefox/34.0',
            'Accept': 'text/plain, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://ru.investing.com/currencies/usd-rub',
            'Connection': 'keep-alive'
        }

    @staticmethod
    def cache_time_to_update():
        """
        :return: interval (in seconds) between update cache
        """
        return 3 * 60  # 3 minutes

    @staticmethod
    def cache_time_to_remove():
        """
        :return: interval (in seconds) while data in cache is stored
        """
        return 60 * 60  # 1 hour