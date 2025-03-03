# Demo project of a python based application which is already present in ECR/ DockerHub repository using KOPS cluster and helm charts

* Pre-requisite - AWS CLI, Image in Dockerhub/ECR

** step 1 - Install helm , kops, Kubectl, AWS CLI - docker image in docker hub private or public repo or AWS ECR repo
 
* Install kops with below command
```
curl -Lo kops https://github.com/kubernetes/kops/releases/download/$(curl -s https://api.github.com/repos/kubernetes/kops/releases/latest | grep tag_name | cut -d '"' -f 4)/kops-linux-amd64
chmod +x kops
sudo mv kops /usr/local/bin/kops
```

 * Install helm with below command
```
curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
sudo apt-get install apt-transport-https --yes
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```

* step 2 : create kops user with necessary permissions
```
aws iam create-group --group-name kops

aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess --group-name kops
aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AmazonRoute53FullAccess --group-name kops
aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess --group-name kops
aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/IAMFullAccess --group-name kops
aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AmazonVPCFullAccess --group-name kops
aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AmazonSQSFullAccess --group-name kops
aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AmazonEventBridgeFullAccess --group-name kops

aws iam create-user --user-name kops

aws iam add-user-to-group --user-name kops --group-name kops

aws iam create-access-key --user-name kops
```
* step 3 : configure above created aws user with aws cli 

* configure the aws client to use your new IAM user
```
aws configure           # Use your new access and secret key here
aws iam list-users      # you should see a list of all your IAM users here
```
* Because "aws configure" doesn't export these vars for kops to use, we export them now
```
export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
export AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
```

* step 4 : create s3 bucket
```
aws s3api create-bucket \
    --bucket prefix-example-com-state-store \ # replace your bucket name
    --region us-east-1
aws s3api put-bucket-versioning --bucket prefix-example-com-state-store  --versioning-configuration Status=Enabled # bucket name
```

* step 5 : create ssh key pair
```
ssh-keygen -t rsa -b 4096 -C "renu@gmail.com"   
```

* step 6 : Export env variables for cluster name and s3 bucket to store cluster configuration file
-> for local dns without any domain purchase
```
export NAME=renucluster.k8s.local  
export KOPS_STATE_STORE=s3://renu-24  # bucket name
```
* step 7 : create kops cluster
```
kops create cluster \
    --name=${NAME} \
    --cloud=aws \
    --zones=us-east-1a

kops validate cluster --wait 10m
```
* after this follow on screen commands - like adding --yes flag wait command for 10 min for cluster creation 
until kops says cluster is ready

* step 8 : check cluster access
```
kubectl get nodes
```
* step 9 : install ingress controller as prerequisite -> this will create ingress controller - ingress class
```
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx

helm repo update

helm install my-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace

verify - kubectl get all -n ingress-nginx
```

* verify ingress controller - deployment - load balancer - pods - ingress class etc

* step 10 : create a helm chart -> this will create a helm chart folder for your application
```
helm create renu-chart  # chartname
# Give values in values.yml --> go to templates and create a secret.yml as below 
helm package renu-chart
helm install myrelease renu-chart # chart name, release name
verify - kubectl get all
verify deployment - serive - pods - ingress are created

```

* step 11 : After demo-project end 

kops delete cluster --name ${NAME} --yes

```
export NAME=renucluster.k8s.local  
export KOPS_STATE_STORE=s3://renu-24
kops delete cluster --name ${NAME} --yes
```

