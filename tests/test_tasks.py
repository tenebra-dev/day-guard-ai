from fastapi.testclient import TestClient
from app.main import app


def test_create_and_list_tasks_with_pagination_and_filters():
    with TestClient(app) as client:
        # create 2 tasks
        payload1 = {"title": "Comprar pão", "location": "mercado", "schedule": "18:00", "mood": "ok"}
        r = client.post("/api/v1/tasks/", json=payload1)
        assert r.status_code == 201

        payload2 = {"title": "Ler livro", "location": "casa", "schedule": "21:00", "mood": "relax"}
        r = client.post("/api/v1/tasks/", json=payload2)
        assert r.status_code == 201

        # list all (default)
        r = client.get("/api/v1/tasks/")
        assert r.status_code == 200
        body = r.json()
        assert "items" in body and isinstance(body["items"], list)
        assert body["total"] >= 2

        # filter by title
        r = client.get("/api/v1/tasks/?title=Comprar")
        assert r.status_code == 200
        body = r.json()
        assert body["total"] >= 1

        # pagination
        r = client.get("/api/v1/tasks/?offset=0&limit=1")
        assert r.status_code == 200
        body = r.json()
        assert body["limit"] == 1
        assert len(body["items"]) <= 1

        # sort
        r = client.get("/api/v1/tasks/?sort_by=title&sort_dir=asc")
        assert r.status_code == 200
        body = r.json()
        titles = [item["title"] for item in body["items"]]
        assert titles == sorted(titles)
