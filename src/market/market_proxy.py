__author__ = 'abodalevsky'

import logging
from time import time
from market.config import Config
from market.connector import get_shares
from market.adapters import response_to_values


class MarketProxy():
    """ Implements proxy for optimization access to online sources

    When request for share is received it checks if data exists in cache:
        - if yes, verifies if data valid (updated):
            - if yes, answer be sent back;
            - if no, all data will be updated, and answer will be sent back;
        - if no, share code be added to cache, all data will be updated, answer will be sent back

    Interface should be similar to Market class


    Contains data that is retrieved from online, in format
        id: [time, answer]
            where:
            time - is time of last request, before update cache from server this info is being analized
                and old data will be removed from the cache
            answer - is in format:
                {
                    'price': float,
                    'summary':string
                },

                for example:
                {
                    '25': [1234567, {'price': 55.640, 'summary':'sell'}],
                    '23': [1234568, {'price': 15.405, 'summary':'buy'}]
                }
    """

    # last time when cache was updated
    __last_update = 0

    def __init__(self):
        self.__cache = dict()
        logging.info('cache: Initialized')

    def get_share(self, code):
        """
        :param code: code {string} of share from class Shares
        :return: value for given share in format
            {
                'price': 55.640,
                'summary':'sell'
            }
        """
        logging.debug('Request for share {0}'.format(code))
        answer = self.__get_from_cache(code)

        if answer == {}:
            self.__add_share_to_cache(code)
            self.__update_cache()
            answer = self.__get_from_cache(code)

        return answer

    def __get_from_cache(self, code):
        """
        Gets data from cache, if data invalid updates cache
        update time to access data, to be sure that data is requested
        :param code: code of share
        :return: answer
        """
        try:
            logging.debug('cache: request')
            answer = self.__cache[code]

            # verify if data is up to dated
            current_time = round(time())
            if current_time - self.__last_update > Config.cache_time_to_update():
                logging.info('cache: out of date')
                self.__update_cache()
                answer = self.__cache[code]

            logging.debug('cache: data returned')
            return answer[1]

        except KeyError:  # no code in the cache
            logging.debug('cache: data not found')
            return {}

    def __add_share_to_cache(self, code):
        """ adds share to cache
        :param code: code of share
        :return: none
        """

        data = self.__format_data_for_cache('0', 'neutral')
        self.__cache[code] = data

    def __update_cache(self):
        """ updates all records in cache
        :return: none
        """

        logging.info('cache: update')

        if len(self.__cache) == 0:
            return

        # prepare list of shares for request
        # check old data, if data is old remove from cache
        shares = str()
        new_cache = dict()
        for i in self.__cache:
            if not self.__should_be_removed(i):
                new_cache[i] = self.__cache[i]
                shares += i + ', '

        self.__cache = new_cache

        # got response in json format
        logging.debug('cache: request for shares[{0}]'.format(shares))
        shares = response_to_values(get_shares(shares.rstrip(', ')))

        self.__last_update = round(time())

        # update cache
        for share, value in shares.items():
            logging.info('cache: update for {0}'.format(share))
            data = self.__format_data_for_cache(value['summaryLast'], value['technicalSummaryClass'])
            self.__cache[share.strip()] = data
            logging.debug('cache: updates with {0}'.format(data))

    def __format_data_for_cache(self, price, recommendation):
        """
        Time will be inserted automatically
        price from string will be converted to float
        :param price: string
        :param recommendation: string
        :return: list
        """

        try:
            pr = round(float(price.replace(',', '.')), 3)
        except ValueError as e:
            logging.error('cache: wrong format: ' + repr(e))
            pr = 0

        return [round(time()), {'price': pr, 'summary': recommendation}]

    def __should_be_removed(self, code):
        last_update = self.__cache[code][0]
        current_time = round(time())
        return current_time - last_update > Config.cache_time_to_remove()
