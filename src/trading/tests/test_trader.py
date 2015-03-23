__author__ = 'abodalevsky'

import unittest
from unittest.mock import *
from trading.trader import Trader


class TestTrader(unittest.TestCase):
    brokers_list = [
        {
            'idbrocker': 1,
            'name': 'FirstBrok',
            'raiting': 5
        },
        {
            'idbrocker': 2,
            'name': 'SecondBrok',
            'raiting': -3
        }
    ]

    brokers_id_list = [1, 2]

    clients_list = [
        {
            'idclients': 125,
            'name': 'CoolClient',
            'balance': 1056.33
        },
    ]

    actives_list = [
        {
            'idactives': 1,
            'code': 8899,
            'quantity': 125365
        },
        {
            'idactives': 5,
            'code': 1,
            'quantity': 1856
        },
        {
            'idactives': 345,
            'code': 8838,
            'quantity': 5365
        },
        {
            'idactives': 456,
            'code': 889,
            'quantity': 365
        },
        {
            'idactives': 792,
            'code': 56,
            'quantity': 6
        },
    ]

    @patch('trading.trader.Store')
    def test_get_brokers_id(self, store_class):
        store_instance = MagicMock()
        store_instance.brokers.return_value = self.brokers_id_list
        store_class.return_value = store_instance

        trader = Trader()
        brokers = trader.get_brokers_id()

        self.assertEqual(2, len(brokers))

    @patch('trading.trader.Store')
    def test_get_brokers(self, store_class):
        store_instance = MagicMock()
        store_instance.brokers.return_value = self.brokers_list
        store_class.return_value = store_instance

        trader = Trader()
        brokers = trader.get_brokers()

        self.assertEqual(self.brokers_list, brokers)
        store_instance.brokers.assert_called_with(True)

    @patch('trading.trader.Store')
    def test_get_clients_for(self, store_class):
        store_instance = MagicMock()
        store_instance.clients.return_value = self.clients_list
        store_class.return_value = store_instance

        trader = Trader()
        clients = trader.get_clients_for(5)

        store_instance.clients.assert_called_with(5)
        self.assertEqual(1, len(clients))

    @patch('trading.trader.Store')
    def test_get_actives(self, store_class):
        store_instance = MagicMock()
        store_instance.actives.return_value = self.actives_list
        store_class.return_value = store_instance

        trader = Trader()
        actives = trader.get_actives_for(3)

        store_instance.actives.assert_called_with(3)
        self.assertEqual(self.actives_list, actives)

    @patch('trading.trader.Store')
    def test_update_active(self, store_class):
        store_instance = MagicMock()
        store_class.return_value = store_instance

        trader = Trader()
        trader.update_active_for(3, 1236)

        store_instance.update_active.assert_called_with(3, 1236)

    @patch('trading.trader.Store')
    def test_update_balance(self, store_class):
        store_instance = MagicMock()
        store_class.return_value = store_instance

        trader = Trader()
        trader.update_balance_for(1, 71236)

        store_instance.update_balance.assert_called_with(1, 71236)

    @patch('trading.trader.Store')
    def test_trade(self, store_class):
        store_instance = MagicMock()
        store_instance.brokers.return_value = self.brokers_id_list  # gets brokers
        store_instance.clients.side_effect = [self.clients_list, []]  # returns clients_list for 1st and empty for 2nd

        store_class.return_value = store_instance

        trader = Trader()
        trader.trade_shares_for = MagicMock()  # replace this method will check that it be called once
        trader.trade()

        self.assertEqual(1, store_instance.brokers.call_count)
        # brokers list should returns 2 items, so client would be called for 2 brokers
        self.assertEqual(2, store_instance.clients.call_count)
        # for 2nd broker list of clients is empty so trade shares would be called once
        self.assertEqual(1, trader.trade_shares_for.call_count)

    def test_trade_client_for(self):
        broker_id = 8
        trade = Trader()

        trade.get_clients_for = MagicMock()
        trade.get_clients_for.return_value = self.clients_list  # 1 client with id: 125
        trade.trade_shares_for = MagicMock()

        trade.trade_client_for(broker_id)

        self.assertEqual([call(broker_id)], trade.get_clients_for.call_args_list)
        # trade_share_for will be called once for client with id:125
        self.assertEqual(1, trade.trade_shares_for.call_count)
        self.assertEqual([call(self.clients_list[0])], trade.trade_shares_for.call_args_list)  # 1&2 are id of brokers

    @patch('trading.trader.Store')
    @patch('trading.trader.Market')
    def test_trade_shares_for(self, market_class, store_class):
        # should be patched:
        # __store.actives(client)
        # __market.get_share(code)
        # client (let say ID: 14) has 2 actives (id: 8899 & 1)
        # market will return values for each requested id
        store_actives_return = [
            {
                'idactives': 2,
                'code': 2186,
                'quantity': 1265
            },
            {
                'idactives': 5,
                'code': 1,
                'quantity': 1856
            }
        ]
        store_instance = MagicMock()
        store_instance.actives.return_value = store_actives_return
        store_class.return_value = store_instance

        market_get_share_return = [
            {
                2186: {
                    'price': 100,
                    'summary': 'buy'
                }
            },
            {
                1: {
                    'price': 26,
                    'summary': 'sell'
                }
            }
        ]
        market_instance = MagicMock()
        market_instance.get_share.side_effect = market_get_share_return
        market_class.return_value = market_instance

        trader_client = {
            'idclients': 14,
            'name': 'CoolClient',
            'balance': 1056.33
        }
        trader = Trader()
        trader.update_balance_for = MagicMock()  # will check that save balance will be called
        trader.update_active_for = MagicMock()  # will check that actives will be saved
        trader.trade_shares_for(trader_client)

        # check that __store.actives() was called for given client
        store_instance.actives.assert_called_with(trader_client['idclients'])

        # check that __market.get_shares() was called twice
        self.assertEqual(2, market_instance.get_share.call_count)
        # first time was passed id: 8899 and second time id:1
        self.assertEqual([call(2186), call(1)], market_instance.get_share.call_args_list)

        # check that save balance was called, based on given data balance should be $911.33
        self.assertEqual(1, trader.update_balance_for.call_count)
        trader.update_balance_for.assert_called_with(trader_client['idclients'], 1176.33)

        # check that update actives was called twice
        self.assertEqual(2, trader.update_active_for.call_count)

        # first time it will be for id:2 quantity:2265
        # second time it will be for id:5 quantity:1855
        self.assertEqual([call(2, 2265), call(5, 1851)], trader.update_active_for.call_args_list)

    @patch('trading.trader.Store')
    @patch('trading.trader.Market')
    def test_trade_shares_for_invalid_market(self, market_class, store_class):
        """
        will test invalid answer from market
        """
        store_actives_return = [
            {
                'idactives': 2,
                'code': 2186,
                'quantity': 1265
            },
            {
                'idactives': 3,
                'code': 2,
                'quantity': 10
            },
            {
                'idactives': 5,
                'code': 1,
                'quantity': 1856
            }
        ]
        store_instance = MagicMock()
        store_instance.actives.return_value = store_actives_return
        store_class.return_value = store_instance

        market_get_share_return = [
            {
                2186: {
                    'price': 100,
                    'summary': 'buy'
                }
            },
            {
                # if something goes wrong the answer will be an empty dict
            },
            {
                1: {
                    'price': 26,
                    'summary': 'sell'
                }
            }
        ]
        market_instance = MagicMock()
        market_instance.get_share.side_effect = market_get_share_return
        market_class.return_value = market_instance

        trader_client = {
            'idclients': 14,
            'name': 'CoolClient',
            'balance': 1056.33
        }
        trader = Trader()
        trader.update_balance_for = MagicMock()  # will check that save balance will be called
        trader.update_active_for = MagicMock()  # will check that actives will be saved
        trader.trade_shares_for(trader_client)

        # check that __store.actives() was called for given client
        store_instance.actives.assert_called_with(trader_client['idclients'])

        # check that __market.get_shares() was called 3 times
        self.assertEqual(3, market_instance.get_share.call_count)
        # passed id: 8899, 2, 1
        self.assertEqual([call(2186), call(2), call(1)], market_instance.get_share.call_args_list)

        # check that save balance was called, based on given data balance should be $911.33
        self.assertEqual(1, trader.update_balance_for.call_count)
        trader.update_balance_for.assert_called_with(trader_client['idclients'], 1176.33)

        # check that update actives was called 3 times
        self.assertEqual(3, trader.update_active_for.call_count)

        # 1st time it will be for id:2 quantity:2265
        # 2nd time it will be for id:3 quantity:10
        # 3rd time it will be for id:5 quantity:1846
        self.assertEqual([call(2, 2265), call(3, 10), call(5, 1851)], trader.update_active_for.call_args_list)
