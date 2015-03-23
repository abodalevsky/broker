from unittest import TestCase

__author__ = 'abodalevsky'

import unittest
from unittest.mock import *
from market.market import Market

ANSWER_FOR_USD_RUB = b'{"topBarAlertEventsCount":1,"js_instrument_chart":{"js_instrument_chart":{"":{"":{"chart_info":"<span id=\\"chart-info-symbol\\" class=\\"arial_16\\"><\\/span><span id=\\"chart-info-arrow\\" class=\\"newSiteIconsSprite a1 greenArrowIcon\\">&nbsp;<\\/span>&nbsp;<span id=\\"chart-info-last\\" class=\\"arial_16 bold\\"><\\/span><span class=\\"arial_14 bold blackFont\\"><span id=\\"chart-info-change\\"><\\/span>(<span id=\\"chart-info-change-percent\\"><\\/span>%)<\\/span>","chart_last_update":null,"chart_data":{"candles":{"last_candle":null,"previous_candle":null},"last_value":null,"last_close_value":null}}}}},"technicalSummaryBox":{"tsb":"{\\"2186\\":{\\"row\\":{\\"last\\":\\"54,639\\",\\"ma\\":\\"\\\\u0410\\\\u043a\\\\u0442\\\\u0438\\\\u0432\\\\u043d\\\\u043e \\\\u043f\\\\u043e\\\\u043a\\\\u0443\\\\u043f\\\\u0430\\\\u0442\\\\u044c\\",\\"ma_class\\":\\"greenFont\\",\\"clock\\":\\"<span class=\\\\\\"greenClockIcon\\\\\\">&nbsp;<\\\\\\/span>\\"},\\"arrowBoxClass\\":\\"downArrow\\",\\"summaryLast\\":\\"54,639\\",\\"summaryName\\":null,\\"summaryNameAlt\\":null,\\"summaryChange\\":\\"-0,001\\",\\"summaryChangePercent\\":\\"-0,00\\",\\"summaryChangeClass\\":\\"redFont\\",\\"technicalSummary\\":\\"\\\\u0410\\\\u043a\\\\u0442\\\\u0438\\\\u0432\\\\u043d\\\\u043e \\\\u043f\\\\u043e\\\\u043a\\\\u0443\\\\u043f\\\\u0430\\\\u0442\\\\u044c\\",\\"technicalSummaryClass\\":\\"buy\\",\\"maBuy\\":12,\\"maSell\\":0,\\"tiBuy\\":5,\\"tiSell\\":3,\\"updateTime\\":\\"24.12 08:34\\",\\"link\\":\\"#\\"}}"}}'
ANSWER_INVALID = b'invalid 12122'
ANSWER_VALID_STRUCTURE_INVALID_PRICE = b'{"topBarAlertEventsCount":1,"js_instrument_chart":{"js_instrument_chart":{"":{"":{"chart_info":"<span id=\\"chart-info-symbol\\" class=\\"arial_16\\"><\\/span><span id=\\"chart-info-arrow\\" class=\\"newSiteIconsSprite a1 greenArrowIcon\\">&nbsp;<\\/span>&nbsp;<span id=\\"chart-info-last\\" class=\\"arial_16 bold\\"><\\/span><span class=\\"arial_14 bold blackFont\\"><span id=\\"chart-info-change\\"><\\/span>(<span id=\\"chart-info-change-percent\\"><\\/span>%)<\\/span>","chart_last_update":null,"chart_data":{"candles":{"last_candle":null,"previous_candle":null},"last_value":null,"last_close_value":null}}}}},"technicalSummaryBox":{"tsb":"{\\"2186\\":{\\"row\\":{\\"last\\":\\"54:639\\",\\"ma\\":\\"\\\\u0410\\\\u043a\\\\u0442\\\\u0438\\\\u0432\\\\u043d\\\\u043e \\\\u043f\\\\u043e\\\\u043a\\\\u0443\\\\u043f\\\\u0430\\\\u0442\\\\u044c\\",\\"ma_class\\":\\"greenFont\\",\\"clock\\":\\"<span class=\\\\\\"greenClockIcon\\\\\\">&nbsp;<\\\\\\/span>\\"},\\"arrowBoxClass\\":\\"downArrow\\",\\"summaryLast\\":\\"54:639\\",\\"summaryName\\":null,\\"summaryNameAlt\\":null,\\"summaryChange\\":\\"-0,001\\",\\"summaryChangePercent\\":\\"-0,00\\",\\"summaryChangeClass\\":\\"redFont\\",\\"technicalSummary\\":\\"\\\\u0410\\\\u043a\\\\u0442\\\\u0438\\\\u0432\\\\u043d\\\\u043e \\\\u043f\\\\u043e\\\\u043a\\\\u0443\\\\u043f\\\\u0430\\\\u0442\\\\u044c\\",\\"technicalSummaryClass\\":\\"buy\\",\\"maBuy\\":12,\\"maSell\\":0,\\"tiBuy\\":5,\\"tiSell\\":3,\\"updateTime\\":\\"24.12 08:34\\",\\"link\\":\\"#\\"}}"}}'
ANSWER_FOR_USD_RUB_OIL_BRENT = b'{"topBarAlertEventsCount":16,"js_instrument_chart":{"js_instrument_chart":{"":{"":{"chart_info":"<span id=\\"chart-info-symbol\\" class=\\"arial_16\\"><\\/span><span id=\\"chart-info-arrow\\" class=\\"newSiteIconsSprite a1 greenArrowIcon\\">&nbsp;<\\/span>&nbsp;<span id=\\"chart-info-last\\" class=\\"arial_16 bold\\"><\\/span><span class=\\"arial_14 bold blackFont\\"><span id=\\"chart-info-change\\"><\\/span>(<span id=\\"chart-info-change-percent\\"><\\/span>%)<\\/span>","chart_last_update":null,"chart_data":{"candles":{"last_candle":null,"previous_candle":null},"last_value":null,"last_close_value":null}}}}},"technicalSummaryBox":{"tsb":"{\\"2186\\":{\\"row\\":{\\"last\\":\\"54,625\\",\\"ma\\":\\"\\\\u0410\\\\u043a\\\\u0442\\\\u0438\\\\u0432\\\\u043d\\\\u043e \\\\u043f\\\\u0440\\\\u043e\\\\u0434\\\\u0430\\\\u0432\\\\u0430\\\\u0442\\\\u044c\\",\\"ma_class\\":\\"redFont\\",\\"clock\\":\\"<span class=\\\\\\"greenClockIcon\\\\\\">&nbsp;<\\\\\\/span>\\"},\\"arrowBoxClass\\":\\"downArrow\\",\\"summaryLast\\":\\"54,625\\",\\"summaryName\\":null,\\"summaryNameAlt\\":null,\\"summaryChange\\":\\"-1,235\\",\\"summaryChangePercent\\":\\"-2,21\\",\\"summaryChangeClass\\":\\"redFont\\",\\"technicalSummary\\":\\"\\\\u0410\\\\u043a\\\\u0442\\\\u0438\\\\u0432\\\\u043d\\\\u043e \\\\u043f\\\\u0440\\\\u043e\\\\u0434\\\\u0430\\\\u0432\\\\u0430\\\\u0442\\\\u044c\\",\\"technicalSummaryClass\\":\\"sell\\",\\"maBuy\\":1,\\"maSell\\":11,\\"tiBuy\\":2,\\"tiSell\\":6,\\"updateTime\\":\\"23.12 17:07\\",\\"link\\":\\"#\\"},\\" 8833\\":{\\"row\\":{\\"last\\":\\"60,76\\",\\"ma\\":null,\\"ma_class\\":\\"redFont\\",\\"clock\\":\\"<span class=\\\\\\"greenClockIcon\\\\\\">&nbsp;<\\\\\\/span>\\"},\\"arrowBoxClass\\":\\"upArrow\\",\\"summaryLast\\":\\"60,76\\",\\"summaryName\\":null,\\"summaryNameAlt\\":null,\\"summaryChange\\":\\"+0,65\\",\\"summaryChangePercent\\":\\"+1,07\\",\\"summaryChangeClass\\":\\"greenFont\\",\\"technicalSummary\\":null,\\"technicalSummaryClass\\":\\"sell\\",\\"maBuy\\":null,\\"maSell\\":null,\\"tiBuy\\":null,\\"tiSell\\":null,\\"updateTime\\":\\"23.12 17:08\\",\\"link\\":\\"#\\"}}"}}'


class TestMarket(unittest.TestCase):
    def setUp(self):
        self.valid_USD_dict = {
            '2186': {
                'price': 54.639,
                'summary': 'buy'
            }
        }

        self.invalid_price_USD_dict = {
            '2186': {
                'price': 0,
                'summary': 'buy'
            }
        }

        self.valid_USD_BRENT_dict = {
            '2186': {
                'price': 54.625,
                'summary': 'sell'
            },
            '8833': {
                'price': 60.76,
                'summary': 'sell'
            }
        }

    @patch('market.market.get_shares')
    def test_market_get_valid(self, get_shares_test_func):
        # replace market.connector.get_shares function with mock that
        # omit connection to internet and returns hardcoded answer
        # used MonkeyPatching technique
        get_shares_test_instance = MagicMock(return_value=ANSWER_FOR_USD_RUB)
        get_shares_test_func.return_value = get_shares_test_instance()

        mr = Market()
        answer = mr.get_share('2186')

        self.assertEqual(self.valid_USD_dict, answer, 'Request data from market failed')
        get_shares_test_func.assert_called_with('2186')

    @patch('market.market.get_shares')
    def test_market_get_invalid(self, get_shares_test_func):
        # replace market.connector.get_shares function with mock that
        # omit connection to internet and returns hardcoded answer
        # used MonkeyPatching technique
        get_shares_test_instance = MagicMock(return_value=ANSWER_INVALID)
        get_shares_test_func.return_value = get_shares_test_instance()

        mr = Market()
        answer = mr.get_share('2186')

        self.assertEqual({}, answer, 'Request data from market failed')
        get_shares_test_func.assert_called_with('2186')

    @patch('market.market.get_shares')
    def test_market_get_wrong_format(self, get_shares_test_func):
        # replace market.connector.get_shares function with mock that
        # omit connection to internet and returns hardcoded answer
        # used MonkeyPatching technique
        get_shares_test_instance = MagicMock(return_value=ANSWER_VALID_STRUCTURE_INVALID_PRICE)
        get_shares_test_func.return_value = get_shares_test_instance()

        mr = Market()
        answer = mr.get_share('2186')

        self.assertEqual(self.invalid_price_USD_dict, answer, 'Request data from market failed')
        get_shares_test_func.assert_called_with('2186')

    @patch('market.market.get_shares')
    def test_market_no_connection(self, get_shares_test_func):
        # replace market.connector.get_shares function with mock that
        # omit connection to internet and returns hardcoded answer
        # used MonkeyPatching technique
        get_shares_test_instance = MagicMock(return_value=None)
        get_shares_test_func.return_value = get_shares_test_instance()

        mr = Market()
        answer = mr.get_share('2186')

        self.assertEqual({}, answer, 'Request data from market failed')
        get_shares_test_func.assert_called_with('2186')

    @patch('market.market.get_shares')
    def test_market_get_list_of_shares(self, get_shares_test_func):
        # replace market.connector.get_shares function with mock that
        # omit connection to internet and returns hardcoded answer
        # used MonkeyPatching technique
        get_shares_test_instance = MagicMock(return_value=ANSWER_FOR_USD_RUB_OIL_BRENT)
        get_shares_test_func.return_value = get_shares_test_instance()

        mr = Market()
        answer = mr.get_share('2186, 8833')

        self.assertEqual(self.valid_USD_BRENT_dict, answer, 'Request data from market failed')
        get_shares_test_func.assert_called_with('2186, 8833')


