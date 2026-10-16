def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "UP"}


def test_ready(client):
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "READY"}


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "TaskBoard API"


def test_create_task(client):
    payload = {
        "title": "Set up CI/CD pipeline",
        "description": "Configure GitHub Actions and Trivy scan",
        "priority": "HIGH",
        "assignee": "Piyush",
    }
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["priority"] == "HIGH"
    assert data["status"] == "TODO"
    assert data["assignee"] == "Piyush"
    assert "id" in data


def test_list_tasks(client):
    client.post("/api/tasks", json={"title": "Task 1", "priority": "LOW"})
    client.post("/api/tasks", json={"title": "Task 2", "priority": "MEDIUM"})
    response = client.get("/api/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2


def test_get_task_by_id(client):
    created = client.post("/api/tasks", json={"title": "Specific Task"}).json()
    response = client.get(f"/api/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Specific Task"


def test_update_task(client):
    created = client.post("/api/tasks", json={"title": "Initial Title"}).json()
    response = client.put(
        f"/api/tasks/{created['id']}",
        json={"title": "Updated Title", "status": "IN_PROGRESS"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"
    assert response.json()["status"] == "IN_PROGRESS"


def test_delete_task(client):
    created = client.post("/api/tasks", json={"title": "To be deleted"}).json()
    response = client.delete(f"/api/tasks/{created['id']}")
    assert response.status_code == 204
    fetch_response = client.get(f"/api/tasks/{created['id']}")
    assert fetch_response.status_code == 404


def test_task_stats(client):
    client.post("/api/tasks", json={"title": "T1", "status": "TODO"})
    client.post("/api/tasks", json={"title": "T2", "status": "IN_PROGRESS"})
    client.post("/api/tasks", json={"title": "T3", "status": "DONE"})
    response = client.get("/api/tasks/stats")
    assert response.status_code == 200
    stats = response.json()
    assert stats["total"] == 3
    assert stats["todo"] == 1
    assert stats["inProgress"] == 1
    assert stats["done"] == 1


def test_task_not_found(client):
    response = client.get("/api/tasks/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
