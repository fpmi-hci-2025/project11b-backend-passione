from fastapi import APIRouter, HTTPException, Query
from uuid import UUID
from typing import Optional, List
from app.database import db
from app.models import Order, OrderCreate, OrderStatus, OrderStatusUpdate, OrderStatusResponse

router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.get("", response_model=dict)
async def get_orders(
    status: Optional[OrderStatus] = None,
    restaurant_id: Optional[UUID] = None
):
    """Получить список заказов (для сотрудников)."""
    orders = db.get_orders(status=status, restaurant_id=restaurant_id)
    return {
        "data": orders,
        "pagination": {"page": 1, "limit": 100, "total": len(orders)}
    }


@router.post("", response_model=Order, status_code=201)
async def create_order(order_data: OrderCreate):
    """Создать заказ из корзины."""
    order = db.create_order(
        session_id=order_data.session_id,
        comment=order_data.comment
    )
    if not order:
        raise HTTPException(
            status_code=400,
            detail="Cannot create order. Check if session exists and cart is not empty."
        )
    return order


@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: UUID):
    """Получить заказ по ID."""
    order = db.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("/{order_id}/status", response_model=OrderStatusResponse)
async def get_order_status(order_id: UUID):
    """Получить статус заказа."""
    order = db.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderStatusResponse(
        order_id=order.id,
        status=order.status,
        updated_at=order.updated_at
    )


@router.patch("/{order_id}/status", response_model=Order)
async def update_order_status(order_id: UUID, status_data: OrderStatusUpdate):
    """Изменить статус заказа (для сотрудников)."""
    order = db.update_order_status(order_id, status_data.status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
