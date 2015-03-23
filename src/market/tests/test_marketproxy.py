from unittest import TestCase
from unittest.mock import *
from market.market_proxy import MarketProxy

__author__ = 'abodalevsky'

"""
b'{"topBarAlertEventsCount":13,"js_instrument_chart":{"js_instrument_chart":{"":{"":{"chart_info":"<span id=\\"chart-info-symbol\\" class=\\"arial_16\\"><\\/span><span id=\\"chart-info-arrow\\" class=\\"newSiteIconsSprite a1 greenArrowIcon\\">&nbsp;<\\/span>&nbsp;<span id=\\"chart-info-last\\" class=\\"arial_16 bold\\"><\\/span><span class=\\"arial_14 bold blackFont\\"><span id=\\"chart-info-change\\"><\\/span>(<span id=\\"chart-info-change-percent\\"><\\/span>%)<\\/span>","chart_last_update":null,"chart_data":{"candles":{"last_candle":null,"previous_candle":null},"last_value":null,"last_close_value":null}}}}},"technicalSummaryBox":{"tsb":"{\\"1\\":{\\"row\\":{\\"last\\":\\"1,1342\\",\\"ma\\":\\"\\\\u041d\\\\u0435\\\\u0439\\\\u0442\\\\u0440\\\\u0430\\\\u043b\\\\u044c\\\\u043d\\\\u043e\\",\\"ma_class\\":\\"neutralFont\\",\\"clock\\":\\"<span class=\\\\\\"greenClockIcon\\\\\\">&nbsp;<\\\\\\/span>\\"},\\"arrowBoxClass\\":\\"downArrow\\",\\"summaryLast\\":\\"1,1342\\",\\"summaryName\\":null,\\"summaryNameAlt\\":null,\\"summaryChange\\":\\"-0,0025\\",\\"summaryChangePercent\\":\\"-0,22\\",\\"summaryChangeClass\\":\\"redFont\\",\\"technicalSummary\\":\\"\\\\u041d\\\\u0435\\\\u0439\\\\u0442\\\\u0440\\\\u0430\\\\u043b\\\\u044c\\\\u043d\\\\u043e\\",\\"technicalSummaryClass\\":\\"neutral\\",\\"maBuy\\":8,\\"maSell\\":4,\\"tiBuy\\":3,\\"tiSell\\":5,\\"updateTime\\":\\"20.02 13:17\\",\\"link\\":\\"#\\"},\\" 3\\":{\\"row\\":{\\"last\\":\\"118,68\\",\\"ma\\":null,\\"ma_class\\":\\"neutralFont\\",\\"clock\\":\\"<span class=\\\\\\"greenClockIcon\\\\\\">&nbsp;<\\\\\\/span>\\"},\\"arrowBoxClass\\":\\"downArrow\\",\\"summaryLast\\":\\"118,68\\",\\"summaryName\\":null,\\"summaryNameAlt\\":null,\\"summaryChange\\":\\"-0,27\\",\\"summaryChangePercent\\":\\"-0,22\\",\\"summaryChangeClass\\":\\"redFont\\",\\"technicalSummary\\":null,\\"technicalSummaryClass\\":\\"neutral\\",\\"maBuy\\":null,\\"maSell\\":null,\\"tiBuy\\":null,\\"tiSell\\":null,\\"updateTime\\":\\"20.02 13:18\\",\\"link\\":\\"#\\"}}"}}'
"""


class TestMarketProxy(TestCase):
    def test_get_share(self):

        proxy = MarketProxy()
        proxy.get_share('3')
        a = proxy.get_share('1')
        #self.assertEqual({}, a)
        pass

    @patch('market.market_proxy.get_shares')
    @patch('market.market_proxy.response_to_values')
    def test_get_share_shares_code_formation(self, r_to_v_test_func, get_shares_test_func):
        """
        verify that list of shares will be formed correctly
        """

        # response_to_value patched just not to call "heavy" original function, we don't need it for this test
        r_to_v_test_instance = MagicMock()
        r_to_v_test_func.return_value = r_to_v_test_instance()

        get_shares_test_instance = MagicMock()
        get_shares_test_func.return_value = get_shares_test_instance()

        proxy = MarketProxy()

        proxy.get_share('1')
        get_shares_test_func.assert_called_with('1')

        proxy.get_share('5')
        called = get_shares_test_func.call_args
        self.assertTrue(self.__compare_list_in_string('1, 5', called[0]))

        proxy.get_share('1')
        called = get_shares_test_func.call_args
        self.assertTrue(self.__compare_list_in_string('1, 5', called[0]))

        proxy.get_share('7')
        called = get_shares_test_func.call_args
        self.assertTrue(self.__compare_list_in_string('1, 5, 7', called[0]))

        proxy.get_share('5')
        called = get_shares_test_func.call_args
        self.assertTrue(self.__compare_list_in_string('1, 5, 7', called[0]))

    def __compare_list_in_string(self, expected, real):
        """ compares 2 strings that represent list in different order, for example
        '1, 2, 3' and '3, 1, 2' result of comparison must be True
        :param expected: string with list '1, 5, 6'
        :param real: tuple first element is string with list '6, 1, 5'
        :return: True if lists are identical (order no matter)
        """
        value, = real

        ex_list = expected.split(', ')
        ex_list.sort()
        re_list = value.split(', ')
        re_list.sort()

        return ex_list == re_list
