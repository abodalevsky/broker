__author__ = 'abodalevsky'

import logging
import sys
from market.config import Config
from time import sleep
from trading.trader import Trader

BANNER = """ Starts trading with interval 5 minutes
    options:
        -storage_host:ip_address - ip address of MySQL server, port is default
        -log:LEVEL - level of output can be:
            CRITICAL = 50
            FATAL = CRITICAL
            ERROR = 40
            WARNING = 30
            WARN = WARNING
            INFO = 20
            DEBUG = 10
            NOTSET = 0
"""


def run():
    logging.basicConfig(format='%(asctime)-15s %(message)s')
    logging.getLogger().setLevel(logging.DEBUG)
    logging.StreamHandler(sys.stdout)

    print(BANNER)
    logging.info('start execution')

    logging.info('Init...')
    Config.init(*sys.argv)
    logging.getLogger().setLevel(Config.LOG_LEVEL)

    t = Trader()

    next_loop = True
    running_count = 1
    while next_loop:
        t.trade()
        print('loop: {0}'.format(running_count))
        sleep(300)
        running_count += 1

    logging.info('end execution')

if __name__ == "__main__":
    run()

