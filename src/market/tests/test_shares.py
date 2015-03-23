from unittest import TestCase
from market.shares import Shares

__author__ = 'abodalevsky'


class TestShares(TestCase):
    def test_get_details(self):
        s = Shares()
        s.get_details(1)
        self.assertEquals({'name': 'EUR-USD', 'for_exchange': 5, 'active_for_exchange': 15, 'usd': True},
                          s.get_details(1))
        self.assertEquals({'name': 'GOLD', 'for_exchange': 1, 'active_for_exchange': 4, 'usd': True},
                          s.get_details('8830'))
        self.assertEquals('Invalid code: False', s.get_details(False))
        self.assertEquals('Invalid code: oil', s.get_details('oil'))

    def test_get_price_in_usd(self):
        s = Shares()

        self.assertAlmostEquals(0.01, s.get_price_in_usd(3, 100))  # for JPY
        self.assertAlmostEquals(0.02, s.get_price_in_usd('2186', 50))  # for RUB
        self.assertAlmostEquals(40, s.get_price_in_usd(1, 40))  # for RUB