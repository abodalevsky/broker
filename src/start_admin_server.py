__author__ = 'abodalevsky'

import bottle
from trading.store import Store
from admin_site.models.client_info import ClientInfo


app = bottle.Bottle()

bottle.TEMPLATE_PATH.insert(0, 'admin_site/views/')


@app.route('/')
def startup():
    return bottle.template('index.html')


@app.route('/welcome')
def welcome():
    return '<h2>Start here</h2>'


@app.route('/static/<path:path>')  # processing static files
def callback(path):
    return bottle.static_file(path, root='admin_site/static/')

@app.route('/get_brokers')
def get_brokers():
    return bottle.template('brokers', brokers=Store().brokers(True))


@app.route('/get_broker/<idb:int>')  # will accept idb as int
def get_broker(idb):
    brokers = Store().brokers(True)
    try:
        return brokers[idb]
    except IndexError:
        bottle.abort(404, 'No broker with id: {0}'. format(idb))


@app.route('/get_clients')
def get_clients():
    return bottle.template('clients', clients=Store().all_clients())


@app.route('/ajax/get_client')
def get_ajax_client():
    t = int(bottle.request.params['id'])  # id of client for test
    return ClientInfo().get_full_info(t)


bottle.run(app, host='172.23.74.56', port=8080, debug=True, reloader=True)
