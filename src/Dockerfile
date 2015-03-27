FROM python:3-onbuild
MAINTAINER abodalevsky@hotmail.com

#address of MySQL
ENV STORAGE_HOST -storage_host:0.0.0.0

#level of logging 
#   CRITICAL = 50
#   ERROR = 40
#   WARNING = 30
#   INFO = 20
#   DEBUG = 10
#   NOTSET = 0
ENV LOG_LEVEL -log:0

RUN rm -rf db/ admin_site/ trading/tests/ market/tests/

CMD python ./runner.py ${STORAGE_HOST} ${LOG_LEVEL}
