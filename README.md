# was_tasks

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