#!/bin/sh
helm repo add apache-airflow https://airflow.apache.org
helm repo update

kubectl create namespace airflow 

helm upgrade --install airflow apache-airflow/airflow -n airflow -f charts/values.yaml

kubectl port-forward svc/airflow-web 8080:8080 -n airflow --address 0.0.0.0 
