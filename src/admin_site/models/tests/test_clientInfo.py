import unittest
from unittest.mock import *

from admin_site.models.client_info import ClientInfo

__author__ = 'abodalevsky'


class TestClientInfo(unittest.TestCase):

    # data received from storage
    client = {
        'name': 'Test Cli',
        'balance': 12345.67
    }

    actives_list = [
        {
          'idactives': 1,
          'code': 3,       # {'name': 'USD-JPU',   'for_exchange': 500,  'active_for_exchange': 700,   'usd': False},
          'quantity': 150
        },
        {
          'idactives': 5,
          'code': 1,        # {'name': 'EUR-USD',   'for_exchange': 5,    'active_for_exchange': 15,    'usd': True},
          'quantity': 150
        },
        {
          'idactives': 7,
          'code': 8830,     # {'name': 'GOLD',      'for_exchange': 1,    'active_for_exchange': 4,     'usd': True},
          'quantity': 150
        }
    ]

    # code is not registered in shares
    bad_active_list = [
       {
          'idactives': 1,
          'code': 999,     # no shares with given code
          'quantity': 1
        }
    ]

    # data that will be returned from tested function
    data_to_return = {
        'name': 'Test Cli',
        'balance': 12345.67,
        'actives': [
            {
                'idactives': 1,
                'code': 3,
                'quantity': 150,
                'details': {
                  'name': 'USD-JPU',
                  'for_exchange': 500,
                  'active_for_exchange': 700,
                  'usd': False
                }
            },
            {
                'idactives': 5,
                'code': 1,
                'quantity': 150,
                'details': {
                   'name': 'EUR-USD',
                   'for_exchange': 5,
                   'active_for_exchange': 15,
                   'usd': True
                }
            },
            {
                'idactives': 7,
                'code': 8830,
                'quantity': 150,
                'details': {
                    'name': 'GOLD',
                    'for_exchange': 1,
                    'active_for_exchange': 4,
                    'usd': True
                }
            }
        ]
    }

    data_to_return_no_active = {
        'name': 'Test Cli',
        'balance': 12345.67,
        'actives': []
    }

    data_to_return_bad_active = {
        'name': 'Test Cli',
        'balance': 12345.67,
        'actives': [
            {
                'idactives': 1,
                'code': 999,
                'quantity': 1,
                'details': 'Invalid code: 999'
            }
        ]
    }

    @patch('admin_site.models.client_info.Store')
    def test_get_full_info(self, store_class):
        store_instance = MagicMock()
        store_instance.client.return_value = self.client
        store_instance.actives.return_value = self.actives_list

        store_class.return_value = store_instance

        client_id = 3

        c = ClientInfo()
        l = c.get_full_info(client_id)

        store_instance.client.assert_called_with(client_id)
        store_instance.actives.assert_called_with(client_id)
        self.assertEqual(self.data_to_return, l)

    @patch('admin_site.models.client_info.Store')
    def test_get_full_info_no_active(self, store_class):
        store_instance = MagicMock()
        store_instance.client.return_value = self.client
        store_instance.actives.return_value = list()

        store_class.return_value = store_instance

        client_id = 3

        c = ClientInfo()
        l = c.get_full_info(client_id)

        self.assertEqual(self.data_to_return_no_active, l)


    @patch('admin_site.models.client_info.Store')
    def test_get_full_info_bad_active(self, store_class):
        store_instance = MagicMock()
        store_instance.client.return_value = self.client
        store_instance.actives.return_value = self.bad_active_list

        store_class.return_value = store_instance

        client_id = 3

        c = ClientInfo()
        l = c.get_full_info(client_id)

        self.assertEqual(self.data_to_return_bad_active, l)
