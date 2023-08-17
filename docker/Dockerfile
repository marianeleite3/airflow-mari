FROM python:3.8-slim

# install deps
RUN apt-get update -y && apt-get install -y \
    libczmq-dev \
    libssl-dev \
    inetutils-telnet \
    bind9utils \
    gcc \
    && apt-get clean

RUN pip install --upgrade pip

RUN pip install apache-airflow
RUN pip install 'apache-airflow[kubernetes]'
RUN pip install 'apache-airflow[postgres]'
RUN pip install 'apache-airflow[google]==2.1.2'
RUN pip install 'apache-airflow-providers-cncf-kubernetes'
RUN pip install 'google-cloud-storage'
RUN pip install 'google-auth'
RUN pip install 'google-auth-oauthlib'
RUN pip install 'requests'
RUN pip install 'google-api-python-client'


COPY airflow-test-env-init.sh /tmp/airflow-test-env-init.sh

COPY bootstrap.sh /bootstrap.sh
RUN chmod +x /bootstrap.sh
ENTRYPOINT ["/bootstrap.sh"]
