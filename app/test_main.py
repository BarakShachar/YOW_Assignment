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


def test_create_user_with_invalid_fields():
    response = client.post(
        "/user/",
        json={"email": "abc", "full_name": "test"},
    )
    assert response.status_code == 422


def test_create_existing_user():
    response = client.post(
        "/user/",
        json={"email": "test@test.com", "full_name": "test test"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "This email already exists"}


def test_create_user_with_optional_fields():
    response = client.post(
        "/user/",
        json={"email": "test1@test.com",
              "full_name": "test test",
              "age": 30
              },
    )
    assert response.status_code == 201
    assert response.json() == {"message": "user created successfully"}


def test_get_user():
    response = client.get("/user/test@test.com")
    assert response.status_code == 200
    assert response.json() == {
        "email": "test@test.com",
        "full_name": "Test Test",
        "age": None
    }


def test_get_user_with_optional_fields():
    response = client.get("/user/test1@test.com")
    assert response.status_code == 200
    assert response.json() == {
        "email": "test1@test.com",
        "full_name": "Test Test",
        "age": 30
    }


def test_get_non_existing_user():
    response = client.get("/user/aaa@aaa.com")
    assert response.status_code == 400
    assert response.json() == {"detail": "no user found for user_email aaa@aaa.com"}


def test_change_user_data():
    response = client.patch(
        "/user/test@test.com",
        json={"full_name": "changed my name",
              "age": 25
              },
    )
    assert response.status_code == 200
    assert response.json() == {"message": "user updated successfully"}


def test_change_non_existing_user_data():
    response = client.patch(
        "/user/aa@aa.com",
        json={"age": 25},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "no user found for user_email aa@aa.com"}


def test_change_user_email_to_existing_email():
    response = client.patch(
        "/user/test@test.com",
        json={"email": "test1@test.com"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "the email test1@test.com already exist"}


def test_delete_user():
    response = client.delete("/user/test@test.com")
    assert response.status_code == 200
    assert response.json() == {"message": "user deleted successfully"}
    client.delete("/user/test1@test.com")


def test_delete_non_existing_user():
    response = client.delete("/user/test@test.com")
    assert response.status_code == 400
    assert response.json() == {"detail": "no user found for user_email test@test.com"}


