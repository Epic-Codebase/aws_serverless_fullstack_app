# aws_tasks

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
