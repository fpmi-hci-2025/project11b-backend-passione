from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime
from uuid import UUID, uuid4


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PREPARING = "PREPARING"
    READY = "READY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class Language(str, Enum):
    RU = "ru"
    EN = "en"


# Dish models
class DishBase(BaseModel):
    name: str
    name_en: Optional[str] = None
    description: Optional[str] = None
    description_en: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    is_available: bool = True
    allergens: List[str] = []
    is_vegetarian: bool = False
    is_vegan: bool = False
    preparation_time: Optional[int] = None


class Dish(DishBase):
    id: UUID = Field(default_factory=uuid4)
    category_id: UUID
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class DishResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    is_available: bool
    allergens: List[str] = []
    is_vegetarian: bool = False
    is_vegan: bool = False
    preparation_time: Optional[int] = None


# Category models
class CategoryBase(BaseModel):
    name: str
    name_en: Optional[str] = None
    description: Optional[str] = None
    sort_order: int = 0
    is_active: bool = True


class Category(CategoryBase):
    id: UUID = Field(default_factory=uuid4)
    menu_id: UUID
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class CategoryWithDishes(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    sort_order: int
    dishes: List[DishResponse] = []


# Menu models
class Menu(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    restaurant_id: UUID
    name: str
    description: Optional[str] = None
    is_active: bool = True


class MenuWithCategories(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    categories: List[CategoryWithDishes] = []


# Restaurant model
class Restaurant(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool = True


# Table model
class Table(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    restaurant_id: UUID
    table_number: str
    qr_code: str
    capacity: Optional[int] = None
    is_active: bool = True


# Session models
class SessionCreate(BaseModel):
    table_id: UUID
    device_id: str
    language: Language = Language.RU


class Session(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    session_token: str
    table_id: UUID
    restaurant_id: UUID
    language: Language = Language.RU
    device_id: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)


# Cart models
class CartItemCreate(BaseModel):
    dish_id: UUID
    quantity: int = Field(ge=1)
    comment: Optional[str] = None


class CartItemUpdate(BaseModel):
    quantity: Optional[int] = Field(ge=1, default=None)
    comment: Optional[str] = None


class CartItem(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    cart_id: UUID
    dish_id: UUID
    quantity: int
    price: float
    comment: Optional[str] = None
    dish: Optional[DishResponse] = None


class Cart(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    session_id: UUID
    total_amount: float = 0
    items: List[CartItem] = []


# Order models
class OrderCreate(BaseModel):
    session_id: UUID
    comment: Optional[str] = None


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class OrderItem(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    order_id: UUID
    dish_id: UUID
    quantity: int
    price: float
    comment: Optional[str] = None
    dish: Optional[DishResponse] = None


class Order(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    restaurant_id: UUID
    table_id: UUID
    session_id: UUID
    table_number: str
    status: OrderStatus = OrderStatus.PENDING
    total_amount: float = 0
    comment: Optional[str] = None
    items: List[OrderItem] = []
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class OrderStatusResponse(BaseModel):
    order_id: UUID
    status: OrderStatus
    updated_at: datetime
