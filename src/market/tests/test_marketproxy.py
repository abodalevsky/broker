from unittest import TestCase
from unittest.mock import *
from market.market_proxy import MarketProxy

__author__ = 'abodalevsky'

"""
b'{"topBarAlertEventsCount":13,"js_instrument_chart":{"js_instrument_chart":{"":{"":{"chart_info":"<span id=\\"chart-info-symbol\\" class=\\"arial_16\\"><\\/span><span id=\\"chart-info-arrow\\" class=\\"newSiteIconsSprite a1 greenArrowIcon\\">&nbsp;<\\/span>&nbsp;<span id=\\"chart-info-last\\" class=\\"arial_16 bold\\"><\\/span><span class=\\"arial_14 bold blackFont\\"><span id=\\"chart-info-change\\"><\\/span>(<span id=\\"chart-info-change-percent\\"><\\/span>%)<\\/span>","chart_last_update":null,"chart_data":{"candles":{"last_candle":null,"previous_candle":null},"last_value":null,"last_close_value":null}}}}},"technicalSummaryBox":{"tsb":"{\\"1\\":{\\"row\\":{\\"last\\":\\"1,1342\\",\\"ma\\":\\"\\\\u041d\\\\u0435\\\\u0439\\\\u0442\\\\u0440\\\\u0430\\\\u043b\\\\u044c\\\\u043d\\\\u043e\\",\\"ma_class\\":\\"neutralFont\\",\\"clock\\":\\"<span class=\\\\\\"greenClockIcon\\\\\\">&nbsp;<\\\\\\/span>\\"},\\"arrowBoxClass\\":\\"downArrow\\",\\"summaryLast\\":\\"1,1342\\",\\"summaryName\\":null,\\"summaryNameAlt\\":null,\\"summaryChange\\":\\"-0,0025\\",\\"summaryChangePercent\\":\\"-0,22\\",\\"summaryChangeClass\\":\\"redFont\\",\\"technicalSummary\\":\\"\\\\u041d\\\\u0435\\\\u0439\\\\u0442\\\\u0440\\\\u0430\\\\u043b\\\\u044c\\\\u043d\\\\u043e\\",\\"technicalSummaryClass\\":\\"neutral\\",\\"maBuy\\":8,\\"maSell\\":4,\\"tiBuy\\":3,\\"tiSell\\":5,\\"updateTime\\":\\"20.02 13:17\\",\\"link\\":\\"#\\"},\\" 3\\":{\\"row\\":{\\"last\\":\\"118,68\\",\\"ma\\":null,\\"ma_class\\":\\"neutralFont\\",\\"clock\\":\\"<span class=\\\\\\"greenClockIcon\\\\\\">&nbsp;<\\\\\\/span>\\"},\\"arrowBoxClass\\":\\"downArrow\\",\\"summaryLast\\":\\"118,68\\",\\"summaryName\\":null,\\"summaryNameAlt\\":null,\\"summaryChange\\":\\"-0,27\\",\\"summaryChangePercent\\":\\"-0,22\\",\\"summaryChangeClass\\":\\"redFont\\",\\"technicalSummary\\":null,\\"technicalSummaryClass\\":\\"neutral\\",\\"maBuy\\":null,\\"maSell\\":null,\\"tiBuy\\":null,\\"tiSell\\":null,\\"updateTime\\":\\"20.02 13:18\\",\\"link\\":\\"#\\"}}"}}'

valid answer for shares 1,3
b'{"topBarAlertEventsCount":0,"js_instrument_chart":{"js_instrument_chart":[]},"technicalSummaryBox":{"tsb":"{\\"3\\":{\\"row\\":{\\"last\\":\\"119,65\\",\\"ma\\":\\"\\\\u041d\\\\u0435\\\\u0439\\\\u0442\\\\u0440\\\\u0430\\\\u043b\\\\u044c\\\\u043d\\\\u043e\\",\\"ma_class\\":\\"neutralFont\\",\\"clock\\":\\"<span class=\\\\\\"greenClockIcon\\\\\\">&nbsp;<\\\\\\/span>\\"},\\"arrowBoxClass\\":\\"downArrow\\",\\"summaryLast\\":\\"119,65\\",\\"summaryName\\":null,\\"summaryNameAlt\\":null,\\"summaryChange\\":\\"-0,11\\",\\"summaryChangePercent\\":\\"-0,09\\",\\"summaryChangeClass\\":\\"redFont\\",\\"technicalSummary\\":\\"\\\\u041d\\\\u0435\\\\u0439\\\\u0442\\\\u0440\\\\u0430\\\\u043b\\\\u044c\\\\u043d\\\\u043e\\",\\"technicalSummaryClass\\":\\"neutral\\",\\"maBuy\\":4,\\"maSell\\":8,\\"tiBuy\\":5,\\"tiSell\\":3,\\"updateTime\\":\\"25.03 11:05\\",\\"link\\":\\"#\\"},\\" 1\\":{\\"row\\":{\\"last\\":\\"1,0947\\",\\"ma\\":null,\\"ma_class\\":\\"neutralFont\\",\\"clock\\":\\"<span class=\\\\\\"greenClockIcon\\\\\\">&nbsp;<\\\\\\/span>\\"},\\"arrowBoxClass\\":\\"upArrow\\",\\"summaryLast\\":\\"1,0947\\",\\"summaryName\\":null,\\"summaryNameAlt\\":null,\\"summaryChange\\":\\"+0,0022\\",\\"summaryChangePercent\\":\\"+0,20\\",\\"summaryChangeClass\\":\\"greenFont\\",\\"technicalSummary\\":null,\\"technicalSummaryClass\\":\\"neutral\\",\\"maBuy\\":null,\\"maSell\\":null,\\"tiBuy\\":null,\\"tiSell\\":null,\\"updateTime\\":\\"25.03 11:04\\",\\"link\\":\\"#\\"}}"}}'

"""


class TestMarketProxy(TestCase):

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

    @patch('market.market_proxy.get_shares')
    def test_update_cache(self, get_shares_test_func):
        VALID_ANSWER = b'{"topBarAlertEventsCount":0,"js_instrument_chart":{"js_instrument_chart":[]},"technicalSummaryBox":{"tsb":"{\\"3\\":{\\"row\\":{\\"last\\":\\"119,65\\",\\"ma\\":\\"\\\\u041d\\\\u0435\\\\u0439\\\\u0442\\\\u0440\\\\u0430\\\\u043b\\\\u044c\\\\u043d\\\\u043e\\",\\"ma_class\\":\\"neutralFont\\",\\"clock\\":\\"<span class=\\\\\\"greenClockIcon\\\\\\">&nbsp;<\\\\\\/span>\\"},\\"arrowBoxClass\\":\\"downArrow\\",\\"summaryLast\\":\\"119,65\\",\\"summaryName\\":null,\\"summaryNameAlt\\":null,\\"summaryChange\\":\\"-0,11\\",\\"summaryChangePercent\\":\\"-0,09\\",\\"summaryChangeClass\\":\\"redFont\\",\\"technicalSummary\\":\\"\\\\u041d\\\\u0435\\\\u0439\\\\u0442\\\\u0440\\\\u0430\\\\u043b\\\\u044c\\\\u043d\\\\u043e\\",\\"technicalSummaryClass\\":\\"neutral\\",\\"maBuy\\":4,\\"maSell\\":8,\\"tiBuy\\":5,\\"tiSell\\":3,\\"updateTime\\":\\"25.03 11:05\\",\\"link\\":\\"#\\"},\\" 1\\":{\\"row\\":{\\"last\\":\\"1,0947\\",\\"ma\\":null,\\"ma_class\\":\\"neutralFont\\",\\"clock\\":\\"<span class=\\\\\\"greenClockIcon\\\\\\">&nbsp;<\\\\\\/span>\\"},\\"arrowBoxClass\\":\\"upArrow\\",\\"summaryLast\\":\\"1,0947\\",\\"summaryName\\":null,\\"summaryNameAlt\\":null,\\"summaryChange\\":\\"+0,0022\\",\\"summaryChangePercent\\":\\"+0,20\\",\\"summaryChangeClass\\":\\"greenFont\\",\\"technicalSummary\\":null,\\"technicalSummaryClass\\":\\"neutral\\",\\"maBuy\\":null,\\"maSell\\":null,\\"tiBuy\\":null,\\"tiSell\\":null,\\"updateTime\\":\\"25.03 11:04\\",\\"link\\":\\"#\\"}}"}}'

        get_shares_test_instance = MagicMock(return_value=VALID_ANSWER)
        get_shares_test_func.return_value = get_shares_test_instance()

        proxy = MarketProxy()

        self.assertEqual(proxy.get_share('1'), {'price': 1.095, 'summary': 'neutral'})
        self.assertEqual(proxy.get_share('3'), {'price': 119.65, 'summary': 'neutral'})

    @patch('market.market_proxy.get_shares')
    def test_update_cache_tsb_null(self, get_shares_test_func):
        get_shares_test_instance = MagicMock(return_value=b'{"technicalSummaryBox" :{ "tsb" : null}}')
        get_shares_test_func.return_value = get_shares_test_instance()

        proxy = MarketProxy()
        self.assertEqual(proxy.get_share('1'), {'price': 0, 'summary': 'neutral'})

    @patch('market.market_proxy.get_shares')
    def test_update_cache_no_connection(self, get_shares_test_func):
        get_shares_test_instance = MagicMock(return_value=None)
        get_shares_test_func.return_value = get_shares_test_instance()

        proxy = MarketProxy()
        self.assertEqual(proxy.get_share('1'), {'price': 0, 'summary': 'neutral'})

    @patch('market.market_proxy.get_shares')
    def test_update_cache_invalid_price(self, get_shares_test_func):
        ANSWER_VALID_STRUCTURE_INVALID_PRICE = b'{"topBarAlertEventsCount":1,"js_instrument_chart":{"js_instrument_chart":{"":{"":{"chart_info":"<span id=\\"chart-info-symbol\\" class=\\"arial_16\\"><\\/span><span id=\\"chart-info-arrow\\" class=\\"newSiteIconsSprite a1 greenArrowIcon\\">&nbsp;<\\/span>&nbsp;<span id=\\"chart-info-last\\" class=\\"arial_16 bold\\"><\\/span><span class=\\"arial_14 bold blackFont\\"><span id=\\"chart-info-change\\"><\\/span>(<span id=\\"chart-info-change-percent\\"><\\/span>%)<\\/span>","chart_last_update":null,"chart_data":{"candles":{"last_candle":null,"previous_candle":null},"last_value":null,"last_close_value":null}}}}},"technicalSummaryBox":{"tsb":"{\\"2186\\":{\\"row\\":{\\"last\\":\\"54:639\\",\\"ma\\":\\"\\\\u0410\\\\u043a\\\\u0442\\\\u0438\\\\u0432\\\\u043d\\\\u043e \\\\u043f\\\\u043e\\\\u043a\\\\u0443\\\\u043f\\\\u0430\\\\u0442\\\\u044c\\",\\"ma_class\\":\\"greenFont\\",\\"clock\\":\\"<span class=\\\\\\"greenClockIcon\\\\\\">&nbsp;<\\\\\\/span>\\"},\\"arrowBoxClass\\":\\"downArrow\\",\\"summaryLast\\":\\"54:639\\",\\"summaryName\\":null,\\"summaryNameAlt\\":null,\\"summaryChange\\":\\"-0,001\\",\\"summaryChangePercent\\":\\"-0,00\\",\\"summaryChangeClass\\":\\"redFont\\",\\"technicalSummary\\":\\"\\\\u0410\\\\u043a\\\\u0442\\\\u0438\\\\u0432\\\\u043d\\\\u043e \\\\u043f\\\\u043e\\\\u043a\\\\u0443\\\\u043f\\\\u0430\\\\u0442\\\\u044c\\",\\"technicalSummaryClass\\":\\"buy\\",\\"maBuy\\":12,\\"maSell\\":0,\\"tiBuy\\":5,\\"tiSell\\":3,\\"updateTime\\":\\"24.12 08:34\\",\\"link\\":\\"#\\"}}"}}'
        get_shares_test_instance = MagicMock(return_value=ANSWER_VALID_STRUCTURE_INVALID_PRICE)
        get_shares_test_func.return_value = get_shares_test_instance()

        proxy = MarketProxy()
        self.assertEqual(proxy.get_share('1'), {'price': 0, 'summary': 'neutral'})

    @patch('market.market_proxy.get_shares')
    def test_update_cache_invalid(self, get_shares_test_func):
        get_shares_test_instance = MagicMock(return_value=b'invalid 12122')
        get_shares_test_func.return_value = get_shares_test_instance()

        proxy = MarketProxy()
        self.assertEqual(proxy.get_share('1'), {'price': 0, 'summary': 'neutral'})


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
