from typing import List
from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts")
    
    def validate(post): # as discionary
        return schemas.PostOut(**post) # unpack and pass as schema
    
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    #print(posts_list[0].Post.id)
    #posts = schemas.PostOut(res.json())# see if we can vlaidate eachpost individually
    assert len(res.json())  == len(test_posts)
    assert res.status_code == 200

def test_unauthorised_user_get_all_posts(client, test_posts):
    res = client.get("/posts")
    assert res.status_code == 401

def test_unauthorised_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/9999999999")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json()) #pydantic validation
    #print(post)
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    assert post.Post.published == test_posts[0].published



@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
    ("tallest guys", "wahoo", True),
    ("tallest gals", "wahoo", True),
    ("tallest dudes", "wahoo", True),
])


def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title": "no publish", "content": "still no publish"})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "no publish"
    assert created_post.content == "still no publish"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']



def test_unauthorised_user_create_posts(client, test_posts):
    res = client.post("/posts/", json={"title": "no publish", "content": "still no publish"})
    assert res.status_code == 401


def test_unauthorised_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_user_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_user_delete_nonexisting_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/9999999999")
    assert res.status_code == 404


def test_user_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[4].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].id

    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].id

    }
    res = authorized_client.put(f"/posts/{test_posts[4].id}", json=data)
    assert res.status_code == 403


def test_unauthorised_user_delete_post(client, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_user_update_nonexisting_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": 99999999

    }
    res = authorized_client.put(f"/posts/999999999999", json=data)
    assert res.status_code == 404

