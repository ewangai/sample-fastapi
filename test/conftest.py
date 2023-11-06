from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app #import from app package
from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base.metadata.create_all(bind=engine) #create tables

#Base = declarative_base()

# Dependency Function
#def override_get_db():
#    db = TestingSessionLocal()
#    try:
#        yield db
#    finally:
#        db.close()
#override every instance of get_db
#app.dependency_overrides[get_db] = override_get_db



#client = TestClient(app) # setting test client to a variable called client.
@pytest.fixture()
def session():
        #run code before we run our test
    Base.metadata.drop_all(bind=engine) #drop tables
    Base.metadata.create_all(bind=engine) #create tables
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    #yield TestClient(app)
    #run code after the test finishes
    #return TestClient(app)
#can also use alembic with command upgrade and downgrade


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    #override every instance of get_db
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    #gives you access to the databse object


@pytest.fixture
def test_user(client): #responsible for creating a test user
    user_data = {"email": "carlosito9@gmail.com", "password": "password123"}   #Define Dictorany with data ot use
    res = client.post("/users/", json=user_data) #store response as json
    assert res.status_code == 201
    #print (res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user
    # rturn details so the tester has this user always available.


@pytest.fixture
def test_user2(client): #responsible for creating a test user
    user_data = {"email": "carlosito10@gmail.com", "password": "password123"}   #Define Dictorany with data ot use
    res = client.post("/users/", json=user_data) #store response as json
    assert res.status_code == 201
    #print (res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user
    # rturn details so the tester has this user always available.


@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture()
def authorized_client(client, token): # take original client and add token
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}" # add one more with auth 
    }
    return client


@pytest.fixture()
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user2['id']
    }]

    
    def create_post_modes(post):
        return models.Post(**post)

    post_map = map(create_post_modes, posts_data)
    posts = list(post_map)

    #can use map function which will iterate into the list and convert it ito a models.post
    #session.add_all([models.Post()]) # multiple add from SQL Alchemy as a list
  

    session.add_all(posts) # multiple add from SQL Alchemy as a list
    session.commit()
    posts = session.query(models.Post).all()
    return posts

