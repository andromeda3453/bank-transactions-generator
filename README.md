# Bank Statement Generator

#### A bank statement generator built using micro-service architecture

##### Technologies used:
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![RabbitMQ](https://img.shields.io/badge/Rabbitmq-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
&nbsp;
## Overview:
##### Each service is standalone and has no direct communication or influence on any other service. Each service can be scaled up or down individually depending on the need. Fault in one service doesn't render other services unusable.
&nbsp;
&nbsp;
## Reasoning for Technologies used: 
### **Python**:
##### Python is one of the most popular programming languages making it extremely well-documented and also easy to use. It has native libraries built for thousands of services which make interacting with them seamless and easy. All of the tasks that were involved in this project were easily implementable using Python. Using one language throughout a project makes interaction between services easier as well and reduces errors and bugs.
&nbsp;
### **RabbitMQ**:
##### Since all services must work independently, A message broken is required to facilitate communication between them. RabbitMQ is a robust, well-documented and widely supported message broker.
&nbsp;
### **FastAPI**:
##### This project includes a trigger API which sets of a chain of operations. FastAPI is a lightweight but also robust and feature rich web API framework for Python. It has many features such as automatic data validation, security and several other features built in. I have used FastAPI previously in projects and have always found it easy to work with.
&nbsp;
### **Pandas**:
##### Pandas is yet another widely supported and performant library for data management and manipulation. It made reading the data from the csv file and filtering it easy and quick. 
&nbsp;
&nbsp;

## Project Architecture: 
&nbsp;
![project_architecture](https://i.imgur.com/u3N8eFa.png)


## Adding Authentication & Authorization:
&nbsp;
#### Authentication: 
##### There are many ways to add authentication to this service. One method which is widely accepted that I would choose would be to use JWTs or Json Web Tokens along with checking for user credentials. After verifying a users credentials against a stored database, they can be issued a JWT that would authenticate further requests. The TTL of the JWT can be controlled and 2FA can also be used to add another layer of security.
&nbsp;
#### Authorization:
##### Authorization is the process of finding what a user has access to. This can also be implemeneted using JWTs but is not ideal (by adding authorization data to the "user claims" in the JWT). Another way is to maintain a list of user roles and assign each user a role which in turn will dictate what resources they have access to (similar to AWS IAM).

 