FROM python:3-onbuild
MAINTAINER abodalevsky@hotmail.com

#address of MySQL
ENV STORAGE_HOST -storage_host:0.0.0.0

RUN rm -rf db/ admin_site/ trading/tests/ market/tests/

CMD python ./runner.py ${STORAGE_HOST}
