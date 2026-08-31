from app.common.models import Item


def test_list_items_empty(client):
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


def test_create_item(client):
    response = client.post("/items", json={"name": "Test Item", "description": "A test"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "A test"
    assert "id" in data


def test_get_item(client, db):
    item = Item(name="Item 1", description="Desc 1")
    db.add(item)
    db.commit()

    response = client.get(f"/items/{item.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Item 1"
    assert data["id"] == item.id


def test_list_items_after_create(client):
    client.post("/items", json={"name": "Item A", "description": "First"})
    client.post("/items", json={"name": "Item B", "description": "Second"})

    response = client.get("/items")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 2
    assert items[0]["name"] == "Item A"
    assert items[1]["name"] == "Item B"


