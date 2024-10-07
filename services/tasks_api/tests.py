import uuid

import boto3
import jwt
import pytest
from fastapi import status
from moto import mock_dynamodb
from starlette.testclient import TestClient

from main import app, get_task_store
from models import Task, TaskStatus
from store import TaskStore


@pytest.fixture
def task_store(dynamodb_table):
    return TaskStore(dynamodb_table)


@pytest.fixture
def client(task_store):
    app.dependency_overrides[get_task_store] = lambda: task_store
    return TestClient(app)


def test_health_check(client):
    """
    GIVEN
    WHEN health check endpoint is called with GET method
    THEN response with status 200 and body OK is returned
    """
    response = client.get("/api/health-check/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "OK"}


@pytest.fixture
def dynamodb_table():
    with mock_dynamodb():
        client = boto3.client("dynamodb")
        table_name = "test-table"
        client.create_table(
            AttributeDefinitions=[
                {"AttributeName": "PK", "AttributeType": "S"},
                {"AttributeName": "SK", "AttributeType": "S"},
                {"AttributeName": "GS1PK", "AttributeType": "S"},
                {"AttributeName": "GS1SK", "AttributeType": "S"},
            ],
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "PK", "KeyType": "HASH"},
                {"AttributeName": "SK", "KeyType": "RANGE"},
            ],
            BillingMode="PAY_PER_REQUEST",
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "GS1",
                    "KeySchema": [
                        {"AttributeName": "GS1PK", "KeyType": "HASH"},
                        {"AttributeName": "GS1SK", "KeyType": "RANGE"},
                    ],
                    "Projection": {
                        "ProjectionType": "ALL",
                    },
                },
            ],
        )
        yield table_name


def test_added_task_retrieved_by_id(dynamodb_table):
    repository = TaskStore(table_name=dynamodb_table)
    task = Task.create(uuid.uuid4(), "Clean your office", "john@doe.com")

    repository.add(task)

    assert repository.get_by_id(task_id=task.id, owner=task.owner) == task


def test_open_tasks_listed(dynamodb_table):
    repository = TaskStore(table_name=dynamodb_table)
    open_task = Task.create(uuid.uuid4(), "Clean your office", "john@doe.com")
    closed_task = Task(
        uuid.uuid4(), "Clean your office", TaskStatus.CLOSED, "john@doe.com"
    )

    repository.add(open_task)
    repository.add(closed_task)

    assert repository.list_open(owner=open_task.owner) == [open_task]


def test_closed_tasks_listed(dynamodb_table):
    repository = TaskStore(table_name=dynamodb_table)
    open_task = Task.create(uuid.uuid4(), "Clean your office", "john@doe.com")
    closed_task = Task(
        uuid.uuid4(), "Clean your office", TaskStatus.CLOSED, "john@doe.com"
    )

    repository.add(open_task)
    repository.add(closed_task)

    assert repository.list_closed(owner=open_task.owner) == [closed_task]


@pytest.fixture
def user_email():
    return "bob@builder.com"


@pytest.fixture
def id_token(user_email):
    return jwt.encode({"cognito:username": user_email}, "secret")


def test_create_task(client, user_email, id_token):
    title = "Clean your desk"
    response = client.post(
        "/api/create-task", json={"title": title}, headers={"Authorization": id_token}
    )
    body = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert body["id"]
    assert body["title"] == title
    assert body["status"] == "OPEN"
    assert body["owner"] == user_email


def test_list_open_tasks(client, user_email, id_token):
    title = "Kiss your wife"
    client.post(
        "/api/create-task", json={"title": title}, headers={"Authorization": id_token}
    )

    response = client.get("/api/open-tasks", headers={"Authorization": id_token})
    body = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert body["results"][0]["id"]
    assert body["results"][0]["title"] == title
    assert body["results"][0]["owner"] == user_email
    assert body["results"][0]["status"] == TaskStatus.OPEN


def test_close_task(client, user_email, id_token):
    title = "Read a book"
    response = client.post(
        "/api/create-task", json={"title": title}, headers={"Authorization": id_token}
    )

    response = client.post(
        "/api/close-task",
        json={"id": response.json()["id"]},
        headers={"Authorization": id_token},
    )
    body = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert body["id"]
    assert body["title"] == title
    assert body["owner"] == user_email
    assert body["status"] == TaskStatus.CLOSED


def test_list_closed_tasks(client, user_email, id_token):
    title = "Ride big waves"
    response = client.post(
        "/api/create-task", json={"title": title}, headers={"Authorization": id_token}
    )
    client.post(
        "/api/close-task",
        json={"id": response.json()["id"]},
        headers={"Authorization": id_token},
    )

    response = client.get("/api/closed-tasks", headers={"Authorization": id_token})
    body = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert body["results"][0]["id"]
    assert body["results"][0]["title"] == title
    assert body["results"][0]["owner"] == user_email
    assert body["results"][0]["status"] == TaskStatus.CLOSED
