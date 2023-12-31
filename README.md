# airflow-mari

This is the repository for deploying airflow on kubernetes.
-----
How was it made:
* For a custom airflow image with instalation of required libraries a custom docker image was built, the image can be found in dockerhub: https://hub.docker.com/repository/docker/mareleite3/airflow/general
  
* The local development was done using KinD: https://kind.sigs.k8s.io/docs/user/quick-start/
* The oficial Helm chart was used for setting up the application with the built image. The Dags are updated via git_sync parameter and the image is using the Kubernetes executor

----
Requirements:

kubectl: https://kubernetes.io/docs/reference/kubectl/kubectl/ 

helm: https://helm.sh/

### How to deploy:
* Clone this repository
* With a Kubernetes cluster and nodes properly configured and acessible with kubectl, run the `.\deploy.sh` in this directory
* After running, the Airflow Web UI will be accessible on `http://localhost:8080.`


  For the DAG running inside the application, it was used GCP for storage, the file was read from the link and uploaded into a bucket.
  The file inside the bucket looks like this:
  ![image](https://github.com/marianeleite3/airflow-mari/assets/87588343/cc3a29de-0498-43f9-bae1-4a9c11ada025)

 
