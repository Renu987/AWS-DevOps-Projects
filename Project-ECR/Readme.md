# Demo of Python based application using CI/CD Pipeline with AWS code build to push the image to ECR and deploying to ECS service.

This project demonstrates a CI/CD pipeline using AWS services to build, push, and deploy a python-based application from a GitHub repository.

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
|   Deploy -ECS
   (Deploy Image )  |
+---------+---------+
          
```


## Configure AWS CodeBuild:
---------------------------
Create ECR Repo (renuka2422

Create an S3 bucket (pipelines-artifacts)

In the AWS Management Console, navigate to the AWS CodeBuild service.

Click on the "Create build project" button.

Provide a name for your build project.

For the source provider, choose GitHub and connect to github.(https://github.com/Renu987/AWS-DevOps-Projects)

Create a service role and attach this poloicies (AmazonSSMFullAccess + AmazonEC2ContainerRegistryFullAccess + AmazonElasticContainerRegistryPublicFullAccess + S3 full access  )

Add build spec file path (Project-ECR/buildspec.yml)

Click on Artifacts --> S3 --> Bucket Name : pipelines-artifacts --> Name : ImageDefinitions ---> path -empty --- Create build project.

Go to AWS systems Manager-->Parameter store --> Add ecr url, docker url, docker username, docker password

Start build --> u can see the image is build and pushed to your ecr repo amd the imagedefinitions.json is stored inside your s3 bucket


## Configure AWS ECS:
-----------------------------

Go to codespace in which aws-cli is installed then aws configure -- connect to your account and perform the below command for ECS configuration

```
aws ecs create-cluster --cluster-name ecs-demo-cluster --region us-east-1   # create a role for ecs task and add that arn in json above

aws ecs register-task-definition --cli-input-json file://task-definition.json # refer the task definition.json file in the repository above

aws ecs create-service --cluster ecs-demo-cluster --service-name ecs-demo-service --task-definition ecs-demo-task --desired-count 1 --launch-type FARGATE --network-configuration "awsvpcConfiguration={subnets=[subnet-0f3ed4adcb1f0d93c],securityGroups=[sg-0c094c32ad6838831],assignPublicIp=ENABLED}" --region us-east-1

# aws ecs update-service --cluster ecs-demo-cluster --service ecs-demo-service --force-new-deployment --region us-east-1

```


##  Configure AWS CodePipeline:
---------------------------------

Give a Name  --> Role -->  Source Provider - GitHub --> Repo URL ---> branch -main

Click on advance config ---> artifact store  - custom location -- s3 bucket - Name -Pipeline-artifacts --> source artifact

Build stage : Above project --> output artifact - build-artifact 

Deploy stage -->Provider-ECS --->cluster name ---> service name --> Input - build artifact --> create

Once Pipeline is successful Go to ECS and click on task --> Public Ip Add :8000 ---> U can see the application output


