from fastapi import APIRouter, HTTPException
from uuid import UUID
from app.database import db
from app.models import Cart, CartItem, CartItemCreate, CartItemUpdate

router = APIRouter(prefix="/api", tags=["Carts"])


@router.get("/carts/{session_id}", response_model=Cart)
async def get_cart(session_id: UUID):
    """Получить корзину по ID сессии."""
    cart = db.get_cart_by_session(session_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.post("/carts/{session_id}/items", response_model=CartItem, status_code=201)
async def add_cart_item(session_id: UUID, item_data: CartItemCreate):
    """Добавить блюдо в корзину."""
    cart_item = db.add_cart_item(
        session_id=session_id,
        dish_id=item_data.dish_id,
        quantity=item_data.quantity,
        comment=item_data.comment
    )
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart or dish not found")
    return cart_item


@router.get("/cart-items/{item_id}", response_model=CartItem)
async def get_cart_item(item_id: UUID):
    """Получить позицию корзины."""
    item = db.cart_items.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return item


@router.patch("/cart-items/{item_id}", response_model=CartItem)
async def update_cart_item(item_id: UUID, item_data: CartItemUpdate):
    """Обновить позицию в корзине."""
    item = db.update_cart_item(
        item_id=item_id,
        quantity=item_data.quantity,
        comment=item_data.comment
    )
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return item


@router.delete("/cart-items/{item_id}", status_code=204)
async def delete_cart_item(item_id: UUID):
    """Удалить позицию из корзины."""
    if not db.delete_cart_item(item_id):
        raise HTTPException(status_code=404, detail="Cart item not found")
