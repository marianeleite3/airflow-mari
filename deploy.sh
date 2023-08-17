#!/bin/sh
helm repo add apache-airflow https://airflow.apache.org
helm repo update
kubectl create namespace airflow

kubectl apply -f charts/persistent-volume.yaml
kubectl apply -f charts/persistent-volume-claim.yaml
helm upgrade --install airflow apache-airflow/airflow -n airflow --values charts/values.yaml --version v1.9.0 --debug

kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow
