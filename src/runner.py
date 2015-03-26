__author__ = 'abodalevsky'

import logging
import sys
from time import sleep
from trading.trader import Trader

BANNER = """ Starts trading with interval 5 minutes"""


def run():
    logging.basicConfig(format='%(asctime)-15s %(message)s')
    logging.getLogger().setLevel(logging.DEBUG)
    logging.StreamHandler(sys.stdout)

    logging.info('start execution')

    t = Trader()
    print(BANNER)

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

