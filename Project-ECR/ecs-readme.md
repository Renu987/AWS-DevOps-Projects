
aws ecs create-cluster --cluster-name ecs-demo-cluster --region us-east-1

aws ecs register-task-definition --cli-input-json file://task-definition.json

create a role ecs task exexution add thatin json above

aws ecs create-service --cluster ecs-demo-cluster --service-name ecs-demo-service --task-definition ecs-demo-task --desired-count 1 --launch-type FARGATE --network-configuration "awsvpcConfiguration={subnets=[subnet-0f3ed4adcb1f0d93c],securityGroups=[sg-0c094c32ad6838831],assignPublicIp=ENABLED}" --region us-east-1

aws ecs update-service --cluster ecs-demo-cluster --service ecs-demo-service --force-new-deployment --region us-east-1

```

{
    "family": "ecs-demo-task",
    "executionRoleArn": "arn:aws:iam::339712876542:role/ecsTaskExecutionRole",
    "networkMode": "awsvpc",
    "containerDefinitions": [
      {
        "name": "ecs-demo-container",
        "image": "339712876542.dkr.ecr.us-east-1.amazonaws.com/renuka2422:code-build",
        "memory": 512,
        "cpu": 256,
        "essential": true,
        "portMappings": [
          {
            "containerPort": 8000,
            "hostPort": 8000
          }
        ]
      }
    ],
    "requiresCompatibilities": [
      "FARGATE"
    ],
    "cpu": "256",
    "memory": "512"
  }
  
```


