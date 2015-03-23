__author__ = 'abodalevsky'

import unittest
from trading.deals import construct_deal_for


class TestDeals(unittest.TestCase):

    def test_nothing(self):
        client = {
            'idclients': 1,
            'name': 'CoolClient',
            'balance': 1000.00
        }

        active = {
            'idactives': 1,
            'code': 8899,
            'quantity': 100
        }

        market_info = {
            '8899': {
                'price': 10,
                'summary': 'neutral'
            }
        }

        share_code = str(active['code'])
        deal = construct_deal_for(market_info[share_code]['summary'])
        deal(client, active, market_info[share_code]['price'])

        self.assertEqual(1000.00, client['balance'])
        self.assertEqual(100, active['quantity'])

    def test_deal_for_buy(self):
        client = {
            'idclients': 1,
            'name': 'CoolClient',
            'balance': 10.50
        }

        active = {
            'idactives': 1,
            'code': 3,
            'quantity': 100
        }

        market_info = {
            '3': {
                'price': 200,
                'summary': 'buy'
            }
        }

        share_code = str(active['code'])
        deal = construct_deal_for(market_info[share_code]['summary'])
        deal(client, active, market_info[share_code]['price'])

        self.assertEqual(8.00, client['balance'])  # it will cost 100$
        self.assertEqual(600, active['quantity'])  # quantity will grow up to 110

    def test_buy_not_enough_money(self):
        client = {
            'idclients': 1,
            'name': 'CoolClient',
            'balance': 10.00
        }

        active = {
            'idactives': 1,
            'code': 8831,
            'quantity': 100
        }

        market_info = {
            '8831': {
                'price': 10,
                'summary': 'buy'
            }
        }

        share_code = str(active['code'])
        deal = construct_deal_for(market_info[share_code]['summary'])
        deal(client, active, market_info[share_code]['price'])

        self.assertEqual(10.00, client['balance'])  # it will cost 100$ but we don't have it
        self.assertEqual(100, active['quantity'])  # quantity won't change

    def test_deal_for_sell(self):
        client = {
            'idclients': 1,
            'name': 'CoolClient',
            'balance': 1000.00
        }

        active = {
            'idactives': 1,
            'code': 8831,
            'quantity': 300
        }

        market_info = {
            '8831': {
                'price': 10,
                'summary': 'sell'
            }
        }

        share_code = str(active['code'])
        deal = construct_deal_for(market_info[share_code]['summary'])
        deal(client, active, market_info[share_code]['price'])

        # be sold 200 shares in total (200 * 10$) = $2000
        self.assertEqual(3000.00, client['balance'])
        self.assertEqual(100, active['quantity'])

    def test_sell_less_then_minimum(self):
        client = {
            'idclients': 1,
            'name': 'CoolClient',
            'balance': 1000.00
        }

        active = {
            'idactives': 1,
            'code': 2186,
            'quantity': 700
        }

        market_info = {
            '2186': {
                'price': 70,
                'summary': 'sell'
            }
        }

        share_code = str(active['code'])
        deal = construct_deal_for(market_info[share_code]['summary'])
        deal(client, active, market_info[share_code]['price'])

        # should be sold 1000 shares, but we have 700 only, therefore
        # will be sold 700 by price $(1/70) in total: $10
        self.assertEqual(1010.00, client['balance'])
        self.assertEqual(0, active['quantity'])  # quantity will be 0
