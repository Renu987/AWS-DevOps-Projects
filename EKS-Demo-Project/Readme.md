# Demo of deploying 2048 Gaming application using Amazon EKS

* keep the devcontainer.json file in the github repo in .devcontainer folder with required features instead of installing everything

* Pre-requisites: 

* Download eksctl in your local using below commands:
```
wget https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_Linux_amd64.tar.gz -O eksctl.tar.gz
tar -xzf eksctl.tar.gz
sudo mv eksctl /usr/local/bin
eksctl version
```
* Download kubectl in your local using below commands:

```
curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
kubectl version --client
```
* Create cluster :
```
eksctl create cluster --name demo-cluster --region us-east-1 --fargate
```
* Create a fargate profile with required namespace:

```
eksctl create fargateprofile --cluster demo-cluster --region us-east-1 --name alb-sample-app --namespace game-2048
```
* Deploy the app file now:
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.5.4/docs/examples/2048/2048_full.yaml

export cluster_name=demo-cluster # cluster name 

oidc_id=$(aws eks describe-cluster --name $cluster_name --query "cluster.identity.oidc.issuer" --output text | cut -d '/' -f 5) 

eksctl utils associate-iam-oidc-provider --cluster $cluster_name --approve

```

* Create IAM role and policy:

```
curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.11.0/docs/install/iam_policy.json

aws iam create-policy \
    --policy-name AWSLoadBalancerControllerIAMPolicy \
    --policy-document file://iam_policy.json

eksctl create iamserviceaccount \
  --cluster=demo-cluster \ # cluster name 
  --namespace=kube-system \
  --name=aws-load-balancer-controller \
  --role-name AmazonEKSLoadBalancerControllerRole \
  --attach-policy-arn=arn:aws:iam::339712876542:policy/AWSLoadBalancerControllerIAMPolicy \ # aws account id 
  --approve
```

* install and add helm:
```
helm repo add eks https://aws.github.io/eks-charts

helm repo update eks

helm install aws-load-balancer-controller eks/aws-load-balancer-controller \            
  -n kube-system \
  --set clusterName=demo-cluster \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller \
  --set region=us-east-1 \
  --set vpcId=vpc-06a28a92dafa7bb0f
```

* Deployment : 
```

kubectl get deployment -n kube-system aws-load-balancer-controller

#if nothing is ready state

#  Reattach IAM policy AWSLoadBalancerControllerIAMPolicy by editing , adding these below lines and save and run below command

{
			"Effect": "Allow",
			"Action": [
				"elasticloadbalancing:DescribeListenerAttributes",
				"elasticloadbalancing:DescribeListeners",
				"elasticloadbalancing:DescribeLoadBalancers",
				"elasticloadbalancing:DescribeRules",
				"elasticloadbalancing:DescribeTags",
				"elasticloadbalancing:DescribeTargetGroups",
				"elasticloadbalancing:DescribeTargetHealth",
				"elasticloadbalancing:ModifyListener",
				"elasticloadbalancing:ModifyRule",
				"elasticloadbalancing:ModifyTargetGroupAttributes",
				"elasticloadbalancing:ModifyLoadBalancerAttributes"
			],
			"Resource": "*"
		}

aws iam attach-role-policy \
    --policy-arn arn:aws:iam::aws:policy/AWSLoadBalancerControllerIAMPolicy \
    --role-name AmazonEKSLoadBalancerControllerRole

kubectl rollout restart deployment aws-load-balancer-controller -n kube-system

```

* check the app output 

```
Go to load balancer ---> click on DNS address --> in browser the app is visible

```
![image](https://github.com/user-attachments/assets/c3dd444d-7c62-4dad-8cae-66f619431535)


* Delete the entire setup once done by using below command:

```
Delete load balancer and target groups manaually first then below command in cmd

eksctl delete cluster --name demo-cluster --region us-east-1

```


