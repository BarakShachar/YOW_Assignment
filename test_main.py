from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/user/",
        json={"email": "test@test.com", "full_name": "test test"},
    )
    assert response.status_code == 201
    assert response.json() == {"message": "user created successfully"}


def test_create_existing_user():
    response = client.post(
        "/user/",
        json={"email": "test@test.com", "full_name": "test test"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": {"error": "This email already exists"}}


def test_create_user_with_additional_fields():
    response = client.post(
        "/user/",
        json={"email": "test1@test.com",
              "full_name": "test test",
              "id": "654654654",
              "age": 30
              },
    )
    assert response.status_code == 201
    assert response.json() == {"message": "user created successfully"}


def test_read_user():
    response = client.get("/user/test@test.com")
    assert response.status_code == 200
    assert response.json() == {
        "email": "test@test.com",
        "full_name": "Test Test",
        "id": None,
        "age": None
    }


def test_delete_user():
    response = client.delete("/user/test@test.com")
    assert response.status_code == 200
    assert response.json() == {"message": "user deleted successfully"}
