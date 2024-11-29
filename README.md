# Managing your personal tasks (both the backend API and frontend UI)

There are a lot of options to choose from when it comes to building a web application. Every step of the way, from the frontend to the backend to deployment, you'll have to choose the tools and technologies. This can be overwhelming.

- Which backend framework? What about the testing library?
- Which JavaScript framework?
- Should I use a SQL or NoSQL database?
- Should I deploy to some cloud provider? Will that cost me a lot?
- What about scalability of my application?
- How should I deploy it? Manually or CI/CD?


### We want to show how to build modern, insanely scalable applications that run on AWS. This project shows how to:

- Build serverless FastAPI APIs that run on AWS Lambda
- Use DynamoDB as the main database for your applications
- Deploy FastAPI apps to AWS Lambda using CI/CD on GitHub Actions and Serverless Framework
- Use Cognito for authentication inside your APIs
- Consume the backend FastAPI API from the frontend Vue application
- Deploy Vue applications to S3
- Use Cognito for authentication inside Vue applications
- Serve your applications with CloudFront CDNs on custom domains
- Set up monitoring and alerting for your applications with CloudWatch

## App overview

Deploys a web application (both the backend API and frontend UI) for managing your personal tasks. We'll cover the following use cases:

- create a task
- list open tasks
- list closed tasks
- close a task

In this git repository, we shall build the API, set up a CI/CD pipeline, build a DynamoDB data model, use Cognito for authentication, build a Vue application, monitor your application, and deploy new versions of the application.

## Tools, Frameworks, and Services

### GitHub
GitHub is a solution for managing the full software development lifecycle. You'll use it for:

- external git repository
- CI/CD pipeline

You can replace it with:

- Bitbucket (with pipelines)
- GitLab
- GitHub + CircleCI

### Poetry
Poetry is a tool used for Python dependency management. You'll use it for managing dependencies.

You can replace it with:

- pip
- pipenv

### FastAPI
FastAPI is a high-performance, easy-to-learn, fast-to-code, ready-for-production web framework for building APIs with Python. You'll use it for building a web application.

You can replace it with:

- Flask
- Django
- Pyramid

### Vue
Vue is a an approachable, performant, and versatile framework for building web user interfaces with JavaScript/TypeScript. You'll use it for building a web application.

You can replace it with:

- React
- Svelte
- Angular

### pytest
The pytest framework makes it easy to write Python tests. You'll use it to write tests for the web application.

You can replace it with:

- unittest
- nose

### AWS DynamoDB
Amazon DynamoDB is "fast, flexible NoSQL database service for single-digit millisecond performance at any scale". You'll use it to persist data used by the web application.

You can replace it with:

- Postgres
- MongoDB

### AWS Cognito
Amazon Cognito is AWS service that simplifies authentication management by a lot. You'll use it sign-up and sign-in your users.

You can replace it with:

- Auth0
- Okta

### AWS Cloudwatch
Amazon CloudWatch is a monitoring and observability service. You'll use it to gather and search logs and monitor resources (like CPU and memory usage) used by the web application.

You can replace it with:

- Prometheus
- Datadog
- New Relic
- Splunk

### AWS Lambda
AWS Lambda is a serverless, event-driven compute service that lets you run code for virtually any type of application or backend service without provisioning or managing servers. You'll use it to run API of your web application.

You can replace it with:

- Azure Functions
- GCP Cloud Functions

### CloudFormation
CloudFormation is an AWS service used to model, provision, and manage AWS resources. You'll use it to manage the AWS infrastructure (DNS, CloudFront, etc.) required for running your application.

You can replace it with:

- Terraform
- Ansible
- Pulumi

### Serverless Framework
Serverless Framework is framework used for developing, deploying, troubleshooting, and securing your serverless applications. You'll use it to manage application resources, like AWS Lambda functions and environment variables, and deploying your applications.

You can replace it with:

- Zappa
- Chalice

### CloudFront
CloudFront is low-latency content delivery network. You'll use it to serve the Vue application from S3 and API from Lambda.

You can replace it with:

- Cloudflare
- Google Cloud CDN
- Microsoft Azure CDN

### Codecov
Codecov is service that helps you track the coverage of your code. You can track changes and compare branches and commits. It helps to focus on changes instead of the current code coverage percentage.

You can replace it with:

- Coveralls
- Github Action Code Coverage Report

### Mangum
Mangum is an adapter for running ASGI applications in AWS Lambda environment. It handles API Gateway events sent to Lambda and responses returned from ASGI application.

## Infrastructure

The easiest way to manage servers, subnets, load balancers, managed databases, etc. is by using infrastructure-as-code (IaC). Inside the "infrastructure" folder we'll store configuration files for our tool(s) of choice. These are usually long YAML, JSON, or HCL files.

## Services

Anything that is long-running or talks to our end users is considered a service. It can be monolithic Django application, Vue UI, or a couple of microservice APIs -- all will reside in this folder.

## Running code-quality locally

Run the code-quality tools before commiting code. There's a validation in the CI/CD that might brake.

```bash
$ poetry run black .
$ poetry run isort . --profile black
$ poetry run flake8 .
```

## Running tests locally

You need to set AWS_DEFAULT_REGION environment variable since Boto3 requires it to be set. Then, run the tests to see the new one fail:

``` bash
$ export AWS_DEFAULT_REGION=eu-west-1
$ poetry run pytest tests.py
```

## Creating the DynamoDB and running the server locally

```bash
export AWS_ACCESS_KEY_ID=abc && export AWS_SECRET_ACCESS_KEY=abc && export AWS_DEFAULT_REGION=eu-west-1 && export TABLE_NAME="local-tasks-api-table" && export DYNAMODB_URL=http://localhost:9999
poetry run python create_dynamodb_locally.py
poetry run uvicorn main:app --reload
```

If you see following error, you only need to give your user the rights of the folder:

```
dynamodb-local  | Oct 07, 2024 8:25:37 PM com.almworks.sqlite4java.Internal log
dynamodb-local  | WARNING: [sqlite] SQLiteQueue[shared-local-instance.db]: stopped abnormally, reincarnating in 3000ms
dynamodb-local  | Oct 07, 2024 8:25:40 PM com.almworks.sqlite4java.Internal log
dynamodb-local  | WARNING: [sqlite] cannot open DB[2]: com.almworks.sqlite4java.SQLiteException: [14] unable to open database file
dynamodb-local  | Oct 07, 2024 8:25:40 PM com.almworks.sqlite4java.Internal log
dynamodb-local  | SEVERE: [sqlite] SQLiteQueue[shared-local-instance.db]: error running job queue
dynamodb-local  | com.almworks.sqlite4java.SQLiteException: [14] unable to open database file
dynamodb-local  | 	at com.almworks.sqlite4java.SQLiteConnection.open0(SQLiteConnection.java:1480)
dynamodb-local  | 	at com.almworks.sqlite4java.SQLiteConnection.open(SQLiteConnection.java:282)
dynamodb-local  | 	at com.almworks.sqlite4java.SQLiteConnection.open(SQLiteConnection.java:293)
dynamodb-local  | 	at com.almworks.sqlite4java.SQLiteQueue.openConnection(SQLiteQueue.java:464)
dynamodb-local  | 	at com.almworks.sqlite4java.SQLiteQueue.queueFunction(SQLiteQueue.java:641)
dynamodb-local  | 	at com.almworks.sqlite4java.SQLiteQueue.runQueue(SQLiteQueue.java:623)
dynamodb-local  | 	at com.almworks.sqlite4java.SQLiteQueue.access$000(SQLiteQueue.java:77)
dynamodb-local  | 	at com.almworks.sqlite4java.SQLiteQueue$1.run(SQLiteQueue.java:205)
dynamodb-local  | 	at java.base/java.lang.Thread.run(Thread.java:840)
dynamodb-local  | 
dynamodb-local  | Oct 07, 2024 8:25:40 PM com.almworks.sqlite4java.Internal log
dynamodb-local  | WARNING: [sqlite] SQLiteQueue[shared-local-instance.db]: stopped abnormally, reincarnating in 3000ms
```

Run the following command in your bash session:

```bash
sudo chown -R $user: docker
```

Where `$user` is your Docker user.

## Testing the server

### Create a task:

```bash
$ curl --location --request POST 'http://localhost:8000/api/create-task' \
--header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2duaXRvOnVzZXJuYW1lIjoiam9obkBkb2UuY29tIn0.6UvNP3lIrXAinXYqH4WzyNrYCxUFIRhAluWyAxcCoUc' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Jump"
}'
```

### List open tasks:

```bash
curl --location --request GET 'http://localhost:8000/api/open-tasks' \
--header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2duaXRvOnVzZXJuYW1lIjoiam9obkBkb2UuY29tIn0.6UvNP3lIrXAinXYqH4WzyNrYCxUFIRhAluWyAxcCoUc'
```
