from fastapi import APIRouter, HTTPException, status
from typing import Dict
from app.models import ItemIn, ItemOut

router = APIRouter(prefix="/items", tags=["Items"])
_fake_db: Dict[int, ItemOut] = {}
_sequence = 1

@router.post(
    "", response_model=ItemOut,
    summary="Create item",
    description="Adds an item; concatenates first_name+last_name and returns it "
                "under `comment` to show tutor-mandated parsing."
)
def create(item: ItemIn):
    global _sequence
    # ----- tutor-spec demo: concatenate two name fields ------------------
    concat = f"{item.first_name}{item.last_name}"
    item.comment = f"auto-concat:{concat}"
    # ---------------------------------------------------------------------
    out = ItemOut(id=_sequence, **item.dict())
    _fake_db[_sequence] = out
    _sequence += 1
    return out

@router.get(
    "/{item_id}", response_model=ItemOut,
    summary="Read item", description="Return one item by id"
)
def read(item_id: int):
    if item_id not in _fake_db:
        raise HTTPException(status_code=404, detail="not found")
    return _fake_db[item_id]

@router.put(
    "/{item_id}", response_model=ItemOut,
    summary="Update item",
    description="Replaces an item; shows same parse+concat trick as POST."
)
def update(item_id: int, item: ItemIn):
    if item_id not in _fake_db:
        raise HTTPException(status_code=404, detail="not found")
    concat = f"{item.first_name}{item.last_name}"
    item.comment = f"auto-concat:{concat}"
    out = ItemOut(id=item_id, **item.dict())
    _fake_db[item_id] = out
    return out

@router.delete(
    "/{item_id}", status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete item", description="Removes an item"
)
def delete(item_id: int):
    _fake_db.pop(item_id, None)
