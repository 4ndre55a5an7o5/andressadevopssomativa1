import pytest

from app import app, tasks


@pytest.fixture(autouse=True)
def reset_tasks_state():
    original_tasks = [
        {"id": 1, "title": "Estudar GitHub Actions", "done": True},
        {"id": 2, "title": "Dockerizar a API", "done": False},
    ]
    tasks.clear()
    tasks.extend(original_tasks)
    yield
    tasks.clear()
    tasks.extend(original_tasks)


def test_home_returns_project_information():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    data = response.get_json()
    assert data["project"] == "DevOps Study API"
    assert data["version"] == "1.0.0"


def test_health_endpoint_returns_ok():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_create_task_with_valid_payload():
    client = app.test_client()
    response = client.post("/tasks", json={"title": "Criar pipeline"})

    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Criar pipeline"
    assert data["done"] is False


def test_create_task_requires_title():
    client = app.test_client()
    response = client.post("/tasks", json={})

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_list_tasks_can_filter_pending_items():
    client = app.test_client()
    response = client.get("/tasks?status=pending")

    assert response.status_code == 200
    data = response.get_json()
    assert all(task["done"] is False for task in data)


def test_list_tasks_returns_all_by_default():
    client = app.test_client()
    response = client.get("/tasks")

    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2


def test_list_tasks_can_filter_done_items():
    client = app.test_client()
    response = client.get("/tasks?status=done")

    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert all(task["done"] is True for task in data)


def test_create_task_trims_title():
    client = app.test_client()
    response = client.post("/tasks", json={"title": "  Nova task  "})

    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Nova task"


def test_create_task_increments_id():
    client = app.test_client()
    response = client.post("/tasks", json={"title": "Task 3"})

    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] == 3
