<!--
title: 'Serverless HTTP AWS API Code'
description: 'Serverless base AWS Python Lambdas'
layout: Doc
framework: v3
platform: AWS
language: python
authorLink: 'https://github.com/serverless'
authorName: 'Serverless, inc.'
authorAvatar: 'https://avatars1.githubusercontent.com/u/13742415?s=200&v=4'
-->

# Serverless HTTP AWS APIs
## Introduction
This application contains 6 HTTP REST APIs with Python running on AWS Lambda and API Gateway using the Serverless Framework.

This application uses DynamoDB to save and persist database
## Setup

### Requirements

This application requires few dependencies to be installed.


- Development Environment: Ubuntu 22.04
- Node.js : Serverless framework requires node to be installed.
- NPM: Node Package Manager: This already come with node(doesn't require installation).

How to install node.js follow link: 
https://nodejs.org/en/download/package-manager#debian-and-ubuntu-based-linux-distributions

Successful installation can be checked with below command:

```
$ node -v 
```
Output:

```
v16.20.2
```

This will give you version of Nodejs installed. Your machine version can be different 

#### Serverless Framework installation

to install serverless framework use below command:

```
$ npm install -g serverless
```

Once your framework is installed, you need to installed serverless plugins with below commands:

```
$ serverless plugin install -n serverless-python-requirements 
$ serverless plugin install -n serverless-iam-roles-per-function
```

#### AWS Credentials setup
This is an important step so follow carefully. Before you can start actual deployment you need to setup your aws account credentials, follow below link below.
https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html
Unless to successfully setup your AWS credentials do not move ahead.

### Execution

To start project execution run below command 

```
$ serverless deploy
```

Which should result in deploying for your  HTTP APIs on AWS and server less will give you list of available api and like below:

```
$ serverless deploy
Running "serverless" from node_modules

Deploying aws-python-http-api-project to stage dev (us-east-1)

✔ Service deployed to stack aws-python-http-api-project-dev (114s)

endpoints:
  GET - https://10ccq2mcl.execute-api.us-east-1.amazonaws.com/dev/health
  POST - https://10ccq2mcl.execute-api.us-east-1.amazonaws.com/dev/users/login
  POST - https://10ccq2mcl.execute-api.us-east-1.amazonaws.com/dev/users/register
  POST - https://10ccq2mcl.execute-api.us-east-1.amazonaws.com/dev/addDevice
  PUT - https://10ccq2mcl.execute-api.us-east-1.amazonaws.com/dev/updateDevice
  POST - https://10ccq2mcl.execute-api.us-east-1.amazonaws.com/dev/addSensor
  GET - https://10ccq2mcl.execute-api.us-east-1.amazonaws.com/dev/getSensorData
  
functions:
  healthCheck: aws-python-http-api-project-dev-healthCheck (254 kB)
  login: aws-python-http-api-project-dev-login (254 kB)
  register: aws-python-http-api-project-dev-register (254 kB)
  addDevice: aws-python-http-api-project-dev-addDevice (254 kB)
  updateDevice: aws-python-http-api-project-dev-updateDevice (254 kB)
  addSensor: aws-python-http-api-project-dev-addSensor (254 kB)
  getSensorData: aws-python-http-api-project-dev-getSensorData (254 kB)

```

### Directory Structure

#### `src` contains python lambda files
#### `vars` contains json files as per environment based e.g. `dev.json`

```
.
├── package.json
├── package-lock.json
├── README.md
├── requirements.txt
├── serverless.yml
├── src
│   ├── add_device.py
│   ├── add_sensor.py
│   ├── auth
│   │   ├── health.py
│   │   ├── __init__.py
│   │   ├── login.py
│   │   └── register.py
│   ├── get_sensor_data.py
│   ├── __init__.py
│   ├── lib
│   │   ├── helper.py
│   │   └── __init__.py
│   ├── __pycache__
│   └── update_device.py
└── vars
    └── dev.json

5 directories, 17 files

```
#### Postman API collection

Under docs folder you will find Postman API collection that you can import in postman for quick execution.

#### NOTE: From Login API, response contains message and JWT Auth token in bearer format like below:

```
"b'ejkfjdjfdjfjdkjfklsjdfkjdsfkjdskfj.hdsfjhjhkjhjkhdsjfhsjkdhfjkhjkhjkhkjdf.sadkjhjkhjkhd'"
```

When using token in postman please use only token-string excluding `b'token-string'`

In case of any query email to proffessional.himanshu@gmail.com 

Thanks

