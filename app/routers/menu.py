from fastapi import APIRouter, HTTPException, Query
from uuid import UUID
from typing import Optional, List
from app.database import db, RESTAURANT_ID
from app.models import Language, DishResponse

router = APIRouter(prefix="/api", tags=["Menu"])


@router.get("/restaurants/{restaurant_id}/menu")
async def get_restaurant_menu(
    restaurant_id: UUID,
    lang: Language = Query(default=Language.RU)
):
    """Получить меню ресторана с категориями и блюдами."""
    menu = db.get_menu_with_categories(restaurant_id, lang)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    return menu


@router.get("/dishes", response_model=dict)
async def get_dishes(
    category_id: Optional[UUID] = None,
    lang: Language = Query(default=Language.RU)
):
    """Получить список блюд."""
    dishes = db.get_dishes(category_id)

    dish_responses = []
    for d in dishes:
        dish_responses.append(DishResponse(
            id=d.id,
            name=d.name_en if lang == Language.EN and d.name_en else d.name,
            description=d.description_en if lang == Language.EN and d.description_en else d.description,
            price=d.price,
            image_url=d.image_url,
            is_available=d.is_available,
            allergens=d.allergens,
            is_vegetarian=d.is_vegetarian,
            is_vegan=d.is_vegan,
            preparation_time=d.preparation_time
        ))

    return {"data": dish_responses, "pagination": {"page": 1, "limit": 100, "total": len(dish_responses)}}


@router.get("/dishes/{dish_id}", response_model=DishResponse)
async def get_dish(
    dish_id: UUID,
    lang: Language = Query(default=Language.RU)
):
    """Получить блюдо по ID."""
    dish = db.get_dish(dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")

    return DishResponse(
        id=dish.id,
        name=dish.name_en if lang == Language.EN and dish.name_en else dish.name,
        description=dish.description_en if lang == Language.EN and dish.description_en else dish.description,
        price=dish.price,
        image_url=dish.image_url,
        is_available=dish.is_available,
        allergens=dish.allergens,
        is_vegetarian=dish.is_vegetarian,
        is_vegan=dish.is_vegan,
        preparation_time=dish.preparation_time
    )
