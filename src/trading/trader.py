__author__ = 'abodalevsky'

import logging
from trading.store import Store
from trading.deals import construct_deal_for
from market.market import Market


class Trader():
    """
    Trader operates with client's actives over market
    """

    def __init__(self):
        self.__store = Store()
        self.__market = Market()

    def get_clients_for(self, broker):
        """
        :param broker: id of broker where clients are searched for
        :return: list of clients in format:{
            'name': 'CoolClient',
            'balance': 1056.33
        }
        """

        return self.__store.clients(broker)

    def get_brokers(self):
        """
        :return: list of brokers (full info, e.g. id, name, rating)
        """

        return self.__store.brokers(True)

    def get_brokers_id(self):
        """
        :return: list of brokers (id only)
        """

        return self.__store.brokers()

    def get_actives_for(self, client):
        """
        returns list of actives for given client, by actives means shares like (oil, gold, currency etc)
        :param client: client's ID
        :return: list of actives in format:{
            'name': 8899,
            'quantity': 125365
        },
        """

        return self.__store.actives(client)

    def update_active_for(self, code, quantity):
        """
        update number of shares for given code
        :param code: code of shares that will be updated
        :param code: new number of shares
        """

        self.__store.update_active(code, quantity)

    def update_balance_for(self, client, new_balance):
        """
        updates balance for given client
        :param client: ID of the client
        :param new_balance: new amount of money
        """

        self.__store.update_balance(client, new_balance)

    def trade(self):
        """
        starts trade procedure for all brokers
        :return:
        """
        logging.info('------------- Start trading -------------')
        for broker in self.get_brokers_id():
            logging.info('---> Broker\'s ID: {0}'.format(broker))
            self.trade_client_for(broker)
        logging.info('------------- end trading -------------')

    def trade_client_for(self, broker):
        """
        requests all clients that belongs to the broker and starts trading
        :param broker: broker's ID
        :return:
        """

        for client in self.get_clients_for(broker):
            logging.info('------> Client: {0}'.format(client))
            self.trade_shares_for(client)

    def trade_shares_for(self, client):
        """
        requests all shares for client, than requests shares prices from market
        and based on market's recommendation trades
        :param client: dict {'idclients':1, 'name':'CL', 'balance':256.33}
        :return:
        """

        # TODO: optimization! Firstly, should be sold all shares to get additional money, then perform buy action

        actives = self.get_actives_for(client['idclients'])
        for active in actives:
            try:  # in case of bad answer from the market will be returned empty dict - will ignore it
                logging.info('Request data for {0}'.format(active))
                share_code = active['code']

                market_share = self.__market.get_share(share_code)  # share_code is string!!!

                # will construct 'deal' abstraction,
                # could be buy/sell/neutral or active buy/sell
                # the abstraction will perform transaction
                info_for_share = market_share[share_code]
                # price = Shares().get_price_in_usd(int(share_code), info_for_share['price'])  # convert to USD
                deal = construct_deal_for(info_for_share['summary'])
                deal(client, active, info_for_share['price'])
                logging.info('Market info for {0}'.format(market_share))
            except KeyError:
                logging.error('Wrong answer for {0}'.format(active['code']))

        # TODO: updated client's balance and shares quantity should be stored as one transaction
        self.update_balance_for(client['idclients'], client['balance'])
        for active in actives:
            self.update_active_for(active['idactives'], active['quantity'])




