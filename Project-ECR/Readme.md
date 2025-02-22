# CI/CD Pipeline with AWS Pushing image to ECR

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
|   Amazon ECR      |
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
Create ECR Repo (renuka2422)

In the AWS Management Console, navigate to the AWS CodeBuild service.

Click on the "Create build project" button.

Provide a name for your build project.

For the source provider, choose GitHub and connect to github.(https://github.com/Renu987/AWS-DevOps-Projects)

Create a service role 

Add build spec file path (AWS-DevOps-Projects/buildspec.yml)

Create build project.

Go to AWS systems Manager-->Parameter store --> Add ecr url.

Go to IAM role and attach AWS SSM full access policy, ECR policy to the created role (AmazonSSMFullAccess + AmazonEC2ContainerRegistryFullAccess + AmazonElasticContainerRegistryPublicFullAccess )

Start build --> u can see the image is build and pushed to your ecr repo.


--------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------

## Configure AWS Code deploy:
-----------------------------


