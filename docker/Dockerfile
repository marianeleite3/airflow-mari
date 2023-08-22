FROM apache/airflow:2.6.2

RUN pip install --upgrade pip

RUN pip install 'apache-airflow[kubernetes]'
RUN pip install 'apache-airflow[postgres]'
RUN pip install 'apache-airflow-providers-cncf-kubernetes'
RUN pip install 'google-cloud-storage'
RUN pip install 'google-auth'
RUN pip install 'google-auth-oauthlib'
RUN pip install 'requests'
RUN pip install 'google-api-python-client'

COPY dags $AIRFLOW_HOME/dags
