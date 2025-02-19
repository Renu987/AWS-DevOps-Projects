# CI/CD Pipeline with AWS Pushing image to Docker Hub 

This project demonstrates a CI/CD pipeline using AWS services to build, push, and deploy a Docker-based application from a GitHub repository.

## Architecture Diagram

```plaintext
+-------------------+
|    GitHub Repo    |
| (Source Code)     |
+---------+---------+
          |
          v
+-------------------+
|   AWS CodePipeline|
|   (Pipeline)      |
+---------+---------+
          |
          v
+-------------------+
|   AWS CodeBuild   |
|   (Build Image)   |
+---------+---------+
          |
          v
+-------------------+
|   DockerHub       |
| (Push Image)      |
+---------+---------+
          |
          v
+-------------------+
|   AWS CodeDeploy  |
|  (Deploy to EC2)  |
+---------+---------+
          |
          v
+-------------------+
|   EC2 Instance    |
| (Run Container)   |
+-------------------+

```


## Configure AWS CodeBuild:
---------------------------

In the AWS Management Console, navigate to the AWS CodeBuild service.

Click on the "Create build project" button.

Provide a name for your build project.

For the source provider, choose GitHub and connect to github.(https://github.com/Renu987/AWS-DevOps-Projects)
Create a service role.
Add build spec file path (Project-DockerHub/buildspec.yml)
Create build project.
Go to AWS systems Manager-->Parameter store --> Add docker url,docker username, docker password.
Go to IAM role and attach AWS SSM full access policy to the created role
Start build --> u can see the image is build and pushed to your docker hub repository.


--------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------

## Configure AWS Code deploy:
-----------------------------

First create an EC2 instance --> add tags --> Attach IAM role (Use case - EC2 ---> AmazonEC2RoleforAWSCodeDeploy + AWSCodeDeployRole)
Connect to EC2 instance and install docker , Agent for Code deploy using below commands :

```plaintext
sudo yum install -y ruby
sudo yum install -y wget
cd /home/ec2-user
wget https://aws-codedeploy-us-west-2.s3.us-west-2.amazonaws.com/latest/install
chmod +x ./install
sudo ./install auto
sudo service codedeploy-agent status (it should be in running state).

```


Go to AWS code deploy --> Application--> Create an application --> EC2
Open created application -->Create Deployment group -->Attach Role (Use case - Code deploy--> AWSCodeDeployRole+EC2 full access)--- IN-Place--EC2 instance--Tag
Create Deployments ---> Deployment grp--->Guthub --> Repo Name (Renu987/AWS-DevOps-Projects) -->commit id (last commit id from github) --> create 
** Make sure the appspec.yml, scripts( startcontainer.sh,stopcontainer.sh) file is in root directory while executing **
