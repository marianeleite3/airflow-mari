# airflow-mari

This is the repository for deploying airflow in kubernetes.
-----
How was it made:
* For a custom airflow image with instalation of required libraries, a docker image was built, the image can be found in dockerhub: https://hub.docker.com/repository/docker/mareleite3/airflow/general
*The local development was done in KinD: https://kind.sigs.k8s.io/docs/user/quick-start/
* The oficial Helm chart was used for setting up the application with the built image

----
How to deploy:
* With a kubernetes cluster and nodes properly configured and acessible with kubectl, run the ./sh in this directory
