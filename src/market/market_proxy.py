__author__ = 'abodalevsky'

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
    """

    """ contains data that is retrieved from online, in format
        id: [time, answer]
            where answer is in format:
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
    def __init__(self):
        self.__cache = dict()

    def get_share(self, code):
        """

        :param code: code {string} of share from class Shares
        :return: value for given share in format
            {
                'price': 55.640,
                'summary':'sell'
            }
        """

        answer = self.__get_from_cache(code)

        if answer == {}:
            self.__add_share_to_cache(code)
            self.__update_cache()
            answer = self.__get_from_cache(code)

        return answer

    def __get_from_cache(self, code):
        """ gets data from cache, if data invalid updates cache
        :param code: code of share
        :return: answer
        """
        try:
            answer = self.__cache[code]

            # verify that data is up to dated
            last_update = answer[0]
            current_time = round(time())
            if current_time - last_update > Config.time_to_update():
                self.__update_cache()
                answer = self.__cache[code]

            return answer[1]

        except KeyError:  # no code in the cache
            return {}

    def __add_share_to_cache(self, code):
        """ adds share to cache
        :param code: code of share
        :return: none
        """

        data = [round(time()), {'price': 0, 'summary':'neutral'}]
        self.__cache[code] = data

    def __update_cache(self):
        """ updates all records in cache
        :return: none
        """

        if len(self.__cache) == 0:
            return

        # prepare list of shares for request
        shares = str()
        for i in self.__cache:
            shares += i + ', '

        shares = response_to_values(get_shares(shares.rstrip(', ')))

        pass