from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_item():
    response = client.get("/recipes/7309c6a3-36d0-45cf-ac4c-daada6155f25")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["name"] == "korean beef"
    
def test_query_by_name():
    response = client.get("/recipes/", params={"name": "korean beef"})
    assert response.status_code == 200
    json_data = response.json()
    assert len(json_data) == 1
    assert json_data[0]["name"] == "korean beef"

def test_query_by_author():
    response = client.get("/recipes/", params={"author": "Joe"})
    assert response.status_code == 200
    json_data = response.json()
    assert len(json_data) == 1
    assert json_data[0]["author"] == "Joe"

def test_query_by_ingredient():
    response = client.get("/recipes/", params={"ingredient": "soy sauce"})
    assert response.status_code == 200
    json_data = response.json()
    assert len(json_data) == 2
    for i in range(len(json_data)):
        assert "soy sauce" in json_data[i]["ingredients"]

def test_query_by_nothing():
    response = client.get("/recipes/")
    assert response.status_code == 200
    json_data = response.json()
    print(json_data)
    assert len(json_data) == 3

# an unmapped query results in the same thing as providing no query item at all
def test_random_query():
    response = client.get("/recipes/", params={"country": "USA"})
    print(response.status_code)
    assert response.status_code == 200
    json_data = response.json()
    print(json_data)
    assert len(json_data) == 3

def test_create_recipe():
    data = {
        "name": "bagel with cream cheese",
        "author": "jonnyboy",
        "ingredients": ["bagel", "cream cheese"],
    }
    response = client.post("/recipes/", json=data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["name"] == "bagel with cream cheese"

def test_update_recipe():
    filler_datetime = datetime.now().isoformat()
    data = {
        "recipe_id":"7309c6a3-36d0-45cf-ac4c-daada6155f25",
        "name": "korean beef",
        "author": "FitzElroy",
        "rating": 5,
        "ingredients": ["ground beef", "soy sauce", "garlic", "ginger"],
        "created_at": filler_datetime,
        "modified_at": filler_datetime
    }
    response = client.put("/recipes/7309c6a3-36d0-45cf-ac4c-daada6155f25", json=data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["author"] == "FitzElroy"

def test_delete_recipe():
    response = client.delete("/recipes/7309c6a3-36d0-45cf-ac4c-daada6155f25")
    assert response.status_code == 200