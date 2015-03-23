__author__ = 'abodalevsky'

import unittest
import market.adapters
import market.connector

ANSWER_FOR_USD_RUB_OIL_BRENT = b'{"topBarAlertEventsCount":16,"js_instrument_chart":{"js_instrument_chart":{"":{"":{"chart_info":"<span id=\\"chart-info-symbol\\" class=\\"arial_16\\"><\\/span><span id=\\"chart-info-arrow\\" class=\\"newSiteIconsSprite a1 greenArrowIcon\\">&nbsp;<\\/span>&nbsp;<span id=\\"chart-info-last\\" class=\\"arial_16 bold\\"><\\/span><span class=\\"arial_14 bold blackFont\\"><span id=\\"chart-info-change\\"><\\/span>(<span id=\\"chart-info-change-percent\\"><\\/span>%)<\\/span>","chart_last_update":null,"chart_data":{"candles":{"last_candle":null,"previous_candle":null},"last_value":null,"last_close_value":null}}}}},"technicalSummaryBox":{"tsb":"{\\"2186\\":{\\"row\\":{\\"last\\":\\"54,625\\",\\"ma\\":\\"\\\\u0410\\\\u043a\\\\u0442\\\\u0438\\\\u0432\\\\u043d\\\\u043e \\\\u043f\\\\u0440\\\\u043e\\\\u0434\\\\u0430\\\\u0432\\\\u0430\\\\u0442\\\\u044c\\",\\"ma_class\\":\\"redFont\\",\\"clock\\":\\"<span class=\\\\\\"greenClockIcon\\\\\\">&nbsp;<\\\\\\/span>\\"},\\"arrowBoxClass\\":\\"downArrow\\",\\"summaryLast\\":\\"54,625\\",\\"summaryName\\":null,\\"summaryNameAlt\\":null,\\"summaryChange\\":\\"-1,235\\",\\"summaryChangePercent\\":\\"-2,21\\",\\"summaryChangeClass\\":\\"redFont\\",\\"technicalSummary\\":\\"\\\\u0410\\\\u043a\\\\u0442\\\\u0438\\\\u0432\\\\u043d\\\\u043e \\\\u043f\\\\u0440\\\\u043e\\\\u0434\\\\u0430\\\\u0432\\\\u0430\\\\u0442\\\\u044c\\",\\"technicalSummaryClass\\":\\"sell\\",\\"maBuy\\":1,\\"maSell\\":11,\\"tiBuy\\":2,\\"tiSell\\":6,\\"updateTime\\":\\"23.12 17:07\\",\\"link\\":\\"#\\"},\\" 8833\\":{\\"row\\":{\\"last\\":\\"60,76\\",\\"ma\\":null,\\"ma_class\\":\\"redFont\\",\\"clock\\":\\"<span class=\\\\\\"greenClockIcon\\\\\\">&nbsp;<\\\\\\/span>\\"},\\"arrowBoxClass\\":\\"upArrow\\",\\"summaryLast\\":\\"60,76\\",\\"summaryName\\":null,\\"summaryNameAlt\\":null,\\"summaryChange\\":\\"+0,65\\",\\"summaryChangePercent\\":\\"+1,07\\",\\"summaryChangeClass\\":\\"greenFont\\",\\"technicalSummary\\":null,\\"technicalSummaryClass\\":\\"sell\\",\\"maBuy\\":null,\\"maSell\\":null,\\"tiBuy\\":null,\\"tiSell\\":null,\\"updateTime\\":\\"23.12 17:08\\",\\"link\\":\\"#\\"}}"}}'


class TestConnector(unittest.TestCase):

    """def test_conn(self):
        jsd = market.connector.get_shares(['USD-RUB'])
        pass
    """

    def test_response_to_values(self):
        analytic = market.adapters.response_to_values(ANSWER_FOR_USD_RUB_OIL_BRENT)
        self.assertEqual(2, len(analytic),
                         'Response should contain 2 records')
        analytic = market.adapters.response_to_values(b'{"good":"but not valid"}')
        self.assertEqual(0, len(analytic),
                         'Response invalid json should contain 0 records')

        analytic = market.adapters.response_to_values(b'{"technicalSummaryBox" :{ "tsb" : null}}')
        self.assertEqual(0, len(analytic),
                         'Response without TSB json should contain 0 records')



