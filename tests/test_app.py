import os

os.environ["USE_GEMINI"] = "false"

os.environ[
    "DATABASE_URL"
] = "sqlite:///./test_fitbuddy.db"

os.environ[
    "ADMIN_KEY"
] = "test-admin"


from fastapi.testclient import TestClient

from app.database import (
    Base,
    engine
)

from app.main import app


Base.metadata.drop_all(
    bind=engine
)

Base.metadata.create_all(
    bind=engine
)


client = TestClient(app)


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json()["status"] == "ok"


def test_home():

    response = client.get("/")

    assert response.status_code == 200

    assert "FitBuddy" in response.text


def test_generate_json_plan():

    response = client.post(

        "/api/users",

        json={

            "username": "Test User",

            "user_id": "TEST001",

            "age": 25,

            "weight": 70,

            "goal": "general wellness",

            "intensity": "medium"
        }
    )


    assert response.status_code == 200


    data = response.json()


    assert (
        data["user"]["user_id"]
        == "TEST001"
    )


    assert (
        "Day 1"
        in data["original_plan"]
    )


def test_feedback_update():

    response = client.post(

        "/api/feedback",

        json={

            "user_id": "TEST001",

            "feedback":
                "Please make the plan easier "
                "and include more recovery."
        }
    )


    assert response.status_code == 200


    assert (
        "UPDATED USING FEEDBACK"
        in response.json()["updated_plan"]
    )


def test_admin():

    response = client.get(
        "/api/users?key=test-admin"
    )


    assert response.status_code == 200

    assert len(response.json()) >= 1