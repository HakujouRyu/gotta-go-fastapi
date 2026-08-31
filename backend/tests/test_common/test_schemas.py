from app.common.models import Item
from app.common.schemas import Item as ItemSchema


def test_item_schema_from_orm():
    item = Item(id=1, name="Test", description="Desc")
    schema = ItemSchema.model_validate(item)
    assert schema.id == 1
    assert schema.name == "Test"
    assert schema.description == "Desc"
