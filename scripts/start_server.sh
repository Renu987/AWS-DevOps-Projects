#!/bin/bash
cd /home/ec2-user/deployment
docker run -d -p 5000:5000 renuka2422/simple-python-flask-app
