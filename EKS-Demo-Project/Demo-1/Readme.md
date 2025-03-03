# Demo for 
* Pre-requisites: Make sure you have kubectl and eksctl installed first to perform this demo

# Connect to your aws account 
```
aws configure

provide access key , secret access key , region, format
```
# create the eks cluster and update kubeconfig ( To Ensure your kubectl is configured to connect to your EKS cluster)

```
eksctl create cluster --name renu-cluster --region us-east-1 --nodegroup-name linux-nodes --node-type t3.medium --nodes 1 --nodes-min 1 --nodes-max 2 --managed

aws eks --region us-east-1 update-kubeconfig --name renu-cluster

```

# create kubernetes deployment and deploy the application  (using deployment.yml)

```
kubectl apply -f deployment.yml

```

# create kubernetes service and apply the service (using service.yml)

```
kubectl apply -f service.yml
```

# check pods (running or not ) and services ( for external ip address)

```
kubectl get deployments

kubectl get services

kubectl get pods

kubectl get service demo-app-service

```

# Access the app through browser

```
Copy the external ip address and and your app exposed port (8000) in browser

```

# Once demo is done delete the cluster :

```
eksctl delete cluster --name renu-cluster --region us-east-1

```
