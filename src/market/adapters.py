__author__ = 'abodalevsky'

import json
import logging


def response_to_values(bdata):
    """Converts received json object to dictionary with shares and its values

    :param bdata: received from market answer
    :return: dictionary contains (share_code, share_value, recommendation)
    """
    try:
        data = bdata.decode('utf-8')
        js_data = json.loads(data)
        tsb = js_data['technicalSummaryBox']
        shares = tsb['tsb']
        if shares is not None:
            js_shares = json.loads(shares)
            return js_shares
        else:
            logging.error('Wrong data format received TSB is None:' + repr(bdata))
            return {}

    except (KeyError, ValueError, AttributeError, TypeError):
        logging.error('Wrong data format received: ' + repr(bdata))
        return {}