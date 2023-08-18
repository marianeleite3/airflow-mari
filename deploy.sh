#!/bin/sh
helm repo add apache-airflow https://airflow.apache.org
helm repo update
kubectl create namespace airflow

helm install airflow apache-airflow/airflow -f charts/values.yaml --namespace airflow

kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow

