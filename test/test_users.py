
import pytest
from jose import jwt
from app import schemas
from app.config import settings

#define fixture to create test user each time

#def test_root(client):
#    res = client.get("/") # not actually running it
#    print(res.json().get('message')) # to return message property
#    assert res.json().get('message') == 'Hello World'
#    #assert res.status_code == 201

#def test_create_user():
#    res = client.post("/users/", json={"email": "carlosito6@gmail.com", "password": "password123"})
#    print(res.json())
#    assert res.json().get("email") == "carlosito6@gmail.com"
#    assert res.status_code == 201

def test_create_user(client):
    res = client.post("/users/", json={"email": "carlosito7@gmail.com", "password": "password123"})
    new_user = schemas.UserOut(**res.json()) # unpack disctionary. This will perform validation 
    assert new_user.email == "carlosito7@gmail.com" # using model
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']}) #form data
    #res = client.post("/login", data={"username": "carlosito7@gmail.com", "password": "password123"}) #form data
    login_res = schemas.Token(**res.json()) # some validation

    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")

    assert id == test_user['id'] # check if ID is the same.
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
                         ('carlosito7@gmail.com', 'wrongpassword', 403),
                         ('wrongemail@gmail.com', 'wrongpassword', 403),
                         ('wrongpassword@gmail.com', 'wrongpassword', 403),
                         (None, 'password123', 422),
                         ('carlosito7@gmail.com', None, 422),
                        ] )

def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    #assert res.json().get('detail') == 'Invalid Credentials'
