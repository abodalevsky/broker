__author__ = 'abodalevsky'

"""
Encapsulates logic of atomic deal for selling or buying some active
"""
import logging
from market.shares import Shares

QUANTITY_FOR_DEAL = 10
QUANTITY_FOR_ACTIVE_DEAL = 25


def construct_deal_for(recommendation):
    """
    will construct function that performs deal based on recommendation (e.g. sell, active buy etc)
    :return function that accepts client, actives and market_info and will perform trading:
    """
    if recommendation == 'buy':
        return deal_for_buy
    elif recommendation == 'sell':
        return deal_for_sell
    else:
        return deal_for_nothing


def deal_for_buy(client, active, market_price):
    """
    performs buy operation
    will allocate money - if enough commit trade otherwise go back without changes
    :return:
    """
    share_catalog = Shares()
    share_details = share_catalog.get_details(active['code'])
    quantity = share_details['for_exchange']
    price_in_usd = share_catalog.get_price_in_usd(active['code'], market_price)
    required_money = price_in_usd * quantity
    if required_money > client['balance']:
        logging.info('DEAL: Not enough money, required: {0}, available {1}'.format(required_money, client['balance']))
        return

    # enough money let's do operation!
    active['quantity'] += quantity
    client['balance'] -= required_money
    logging.info(
        'DEAL: buy committed! \n\t bought: {0} by price: {1} in total: {2} \n\t total active: {3},  balance: {4}'.format(
            quantity, market_price, required_money, active['quantity'], client['balance']))


def deal_for_sell(client, active, market_price):
    """
    performs sell operation
    :return:
    """
    share_catalog = Shares()
    share_details = share_catalog.get_details(active['code'])
    quantity = share_details['for_exchange']
    shares_to_sell = quantity if active['quantity'] >= quantity else active['quantity']
    price_in_usd = share_catalog.get_price_in_usd(active['code'], market_price)  # recalculate price in USD
    money = shares_to_sell * price_in_usd
    active['quantity'] -= shares_to_sell
    client['balance'] += money
    logging.info(
        'DEAL: sell committed! \n\t sold: {0} by price: {1} in total: {2}\n\t total active: {3},  balance: {4}'.format(
            shares_to_sell, market_price, money, active['quantity'], client['balance']))


def deal_for_nothing(client, active, cost):
    """
    performs nothing, no any values will be changed
    incoming parameters are saved for interface compatibility with functions for selling/buying
    :return:
    """
    logging.info('DEAL: no changes')
