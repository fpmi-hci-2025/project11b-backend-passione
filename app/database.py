"""
In-memory database with demo data for Passione restaurant.
"""
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from app.models import (
    Restaurant, Menu, Category, Dish, Table, Session,
    Cart, CartItem, Order, OrderItem, OrderStatus, Language, DishResponse
)

# Demo UUIDs
RESTAURANT_ID = UUID("11111111-1111-1111-1111-111111111111")
MENU_ID = UUID("22222222-2222-2222-2222-222222222222")
TABLE_1_ID = UUID("33333333-3333-3333-3333-333333333331")
TABLE_2_ID = UUID("33333333-3333-3333-3333-333333333332")

# Categories
CAT_ANTIPASTI_ID = UUID("44444444-4444-4444-4444-444444444441")
CAT_PRIMI_ID = UUID("44444444-4444-4444-4444-444444444442")
CAT_SECONDI_ID = UUID("44444444-4444-4444-4444-444444444443")
CAT_DOLCI_ID = UUID("44444444-4444-4444-4444-444444444444")
CAT_BEVANDE_ID = UUID("44444444-4444-4444-4444-444444444445")

# Dishes
DISH_BRUSCHETTA_ID = UUID("55555555-5555-5555-5555-555555555501")
DISH_CARPACCIO_ID = UUID("55555555-5555-5555-5555-555555555502")
DISH_CAPRESE_ID = UUID("55555555-5555-5555-5555-555555555503")
DISH_SPAGHETTI_ID = UUID("55555555-5555-5555-5555-555555555504")
DISH_RISOTTO_ID = UUID("55555555-5555-5555-5555-555555555505")
DISH_LASAGNA_ID = UUID("55555555-5555-5555-5555-555555555506")
DISH_SALMON_ID = UUID("55555555-5555-5555-5555-555555555507")
DISH_STEAK_ID = UUID("55555555-5555-5555-5555-555555555508")
DISH_TIRAMISU_ID = UUID("55555555-5555-5555-5555-555555555509")
DISH_PANNA_COTTA_ID = UUID("55555555-5555-5555-5555-555555555510")
DISH_ESPRESSO_ID = UUID("55555555-5555-5555-5555-555555555511")
DISH_WINE_ID = UUID("55555555-5555-5555-5555-555555555512")


class Database:
    def __init__(self):
        self.restaurants: Dict[UUID, Restaurant] = {}
        self.menus: Dict[UUID, Menu] = {}
        self.categories: Dict[UUID, Category] = {}
        self.dishes: Dict[UUID, Dish] = {}
        self.tables: Dict[UUID, Table] = {}
        self.sessions: Dict[UUID, Session] = {}
        self.carts: Dict[UUID, Cart] = {}
        self.cart_items: Dict[UUID, CartItem] = {}
        self.orders: Dict[UUID, Order] = {}
        self.order_items: Dict[UUID, OrderItem] = {}

        self._init_demo_data()

    def _init_demo_data(self):
        # Restaurant
        restaurant = Restaurant(
            id=RESTAURANT_ID,
            name="Passione",
            address="ул. Итальянская, 15, Москва",
            phone="+7 (495) 123-45-67"
        )
        self.restaurants[restaurant.id] = restaurant

        # Menu
        menu = Menu(
            id=MENU_ID,
            restaurant_id=RESTAURANT_ID,
            name="Основное меню",
            description="Блюда итальянской кухни"
        )
        self.menus[menu.id] = menu

        # Tables
        for i, table_id in enumerate([TABLE_1_ID, TABLE_2_ID], 1):
            table = Table(
                id=table_id,
                restaurant_id=RESTAURANT_ID,
                table_number=str(i),
                qr_code=f"passione-table-{i}",
                capacity=4
            )
            self.tables[table.id] = table

        # Categories
        categories_data = [
            (CAT_ANTIPASTI_ID, "Антипасти", "Antipasti", "Итальянские закуски", 1),
            (CAT_PRIMI_ID, "Первые блюда", "Primi Piatti", "Паста и ризотто", 2),
            (CAT_SECONDI_ID, "Вторые блюда", "Secondi Piatti", "Мясо и рыба", 3),
            (CAT_DOLCI_ID, "Десерты", "Dolci", "Сладости", 4),
            (CAT_BEVANDE_ID, "Напитки", "Bevande", "Кофе и вино", 5),
        ]

        for cat_id, name, name_en, desc, order in categories_data:
            cat = Category(
                id=cat_id,
                menu_id=MENU_ID,
                name=name,
                name_en=name_en,
                description=desc,
                sort_order=order
            )
            self.categories[cat.id] = cat

        # Dishes
        dishes_data = [
            # Antipasti
            (DISH_BRUSCHETTA_ID, CAT_ANTIPASTI_ID, "Брускетта с томатами", "Bruschetta with tomatoes",
             "Хрустящий хлеб с свежими томатами и базиликом",
             "Crispy bread with fresh tomatoes and basil", 450, True, True, 10, []),
            (DISH_CARPACCIO_ID, CAT_ANTIPASTI_ID, "Карпаччо из говядины", "Beef Carpaccio",
             "Тонко нарезанная говядина с рукколой и пармезаном",
             "Thinly sliced beef with arugula and parmesan", 890, False, False, 15, ["молоко"]),
            (DISH_CAPRESE_ID, CAT_ANTIPASTI_ID, "Капрезе", "Caprese",
             "Моцарелла с томатами и базиликом",
             "Mozzarella with tomatoes and basil", 650, True, False, 10, ["молоко"]),

            # Primi
            (DISH_SPAGHETTI_ID, CAT_PRIMI_ID, "Спагетти Карбонара", "Spaghetti Carbonara",
             "Спагетти с беконом, яйцом и пармезаном",
             "Spaghetti with bacon, egg and parmesan", 750, False, False, 20, ["глютен", "яйца", "молоко"]),
            (DISH_RISOTTO_ID, CAT_PRIMI_ID, "Ризотто с грибами", "Mushroom Risotto",
             "Кремовое ризотто с белыми грибами",
             "Creamy risotto with porcini mushrooms", 820, True, False, 25, ["молоко"]),
            (DISH_LASAGNA_ID, CAT_PRIMI_ID, "Лазанья Болоньезе", "Lasagna Bolognese",
             "Классическая лазанья с мясным рагу",
             "Classic lasagna with meat sauce", 890, False, False, 30, ["глютен", "молоко"]),

            # Secondi
            (DISH_SALMON_ID, CAT_SECONDI_ID, "Лосось на гриле", "Grilled Salmon",
             "Филе лосося с овощами гриль",
             "Salmon fillet with grilled vegetables", 1450, False, False, 25, ["рыба"]),
            (DISH_STEAK_ID, CAT_SECONDI_ID, "Стейк Рибай", "Ribeye Steak",
             "Стейк из мраморной говядины 300г",
             "Marble beef steak 300g", 2200, False, False, 30, []),

            # Dolci
            (DISH_TIRAMISU_ID, CAT_DOLCI_ID, "Тирамису", "Tiramisu",
             "Классический итальянский десерт",
             "Classic Italian dessert", 490, True, False, 5, ["глютен", "яйца", "молоко"]),
            (DISH_PANNA_COTTA_ID, CAT_DOLCI_ID, "Панна Котта", "Panna Cotta",
             "Сливочный десерт с ягодным соусом",
             "Cream dessert with berry sauce", 420, True, False, 5, ["молоко"]),

            # Bevande
            (DISH_ESPRESSO_ID, CAT_BEVANDE_ID, "Эспрессо", "Espresso",
             "Классический итальянский кофе",
             "Classic Italian coffee", 180, True, True, 3, []),
            (DISH_WINE_ID, CAT_BEVANDE_ID, "Вино Кьянти (бокал)", "Chianti Wine (glass)",
             "Красное итальянское вино",
             "Italian red wine", 450, True, True, 2, []),
        ]

        # Real food images from Unsplash
        dish_images = {
            DISH_BRUSCHETTA_ID: "https://images.unsplash.com/photo-1572695157366-5e585ab2b69f?w=400&h=300&fit=crop",
            DISH_CARPACCIO_ID: "https://images.unsplash.com/photo-1588168333986-5078d3ae3976?w=400&h=300&fit=crop",
            DISH_CAPRESE_ID: "https://images.unsplash.com/photo-1608897013039-887f21d8c804?w=400&h=300&fit=crop",
            DISH_SPAGHETTI_ID: "https://images.unsplash.com/photo-1612874742237-6526221588e3?w=400&h=300&fit=crop",
            DISH_RISOTTO_ID: "https://images.unsplash.com/photo-1476124369491-e7addf5db371?w=400&h=300&fit=crop",
            DISH_LASAGNA_ID: "https://images.unsplash.com/photo-1574894709920-11b28e7367e3?w=400&h=300&fit=crop",
            DISH_SALMON_ID: "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=400&h=300&fit=crop",
            DISH_STEAK_ID: "https://images.unsplash.com/photo-1600891964092-4316c288032e?w=400&h=300&fit=crop",
            DISH_TIRAMISU_ID: "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=400&h=300&fit=crop",
            DISH_PANNA_COTTA_ID: "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400&h=300&fit=crop",
            DISH_ESPRESSO_ID: "https://images.unsplash.com/photo-1510707577719-ae7c14805e3a?w=400&h=300&fit=crop",
            DISH_WINE_ID: "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=400&h=300&fit=crop",
        }

        for dish_data in dishes_data:
            dish_id, cat_id, name, name_en, desc, desc_en, price, veg, vegan, prep_time, allergens = dish_data
            dish = Dish(
                id=dish_id,
                category_id=cat_id,
                name=name,
                name_en=name_en,
                description=desc,
                description_en=desc_en,
                price=price,
                is_vegetarian=veg,
                is_vegan=vegan,
                preparation_time=prep_time,
                allergens=allergens,
                image_url=dish_images.get(dish_id, f"https://via.placeholder.com/400x300?text={name_en.replace(' ', '+')}")
            )
            self.dishes[dish.id] = dish

    # Restaurant methods
    def get_restaurant(self, restaurant_id: UUID) -> Optional[Restaurant]:
        return self.restaurants.get(restaurant_id)

    # Menu methods
    def get_menu_by_restaurant(self, restaurant_id: UUID) -> Optional[Menu]:
        for menu in self.menus.values():
            if menu.restaurant_id == restaurant_id and menu.is_active:
                return menu
        return None

    def get_menu_with_categories(self, restaurant_id: UUID, lang: Language = Language.RU):
        menu = self.get_menu_by_restaurant(restaurant_id)
        if not menu:
            return None

        categories = sorted(
            [c for c in self.categories.values() if c.menu_id == menu.id and c.is_active],
            key=lambda x: x.sort_order
        )

        categories_with_dishes = []
        for cat in categories:
            dishes = [d for d in self.dishes.values() if d.category_id == cat.id and d.is_available]

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

            categories_with_dishes.append({
                "id": cat.id,
                "name": cat.name_en if lang == Language.EN and cat.name_en else cat.name,
                "description": cat.description,
                "sort_order": cat.sort_order,
                "dishes": dish_responses
            })

        return {
            "id": menu.id,
            "name": menu.name,
            "description": menu.description,
            "categories": categories_with_dishes
        }

    # Dish methods
    def get_dish(self, dish_id: UUID) -> Optional[Dish]:
        return self.dishes.get(dish_id)

    def get_dishes(self, category_id: Optional[UUID] = None) -> List[Dish]:
        dishes = list(self.dishes.values())
        if category_id:
            dishes = [d for d in dishes if d.category_id == category_id]
        return dishes

    # Table methods
    def get_table(self, table_id: UUID) -> Optional[Table]:
        return self.tables.get(table_id)

    def get_table_by_qr(self, qr_code: str) -> Optional[Table]:
        for table in self.tables.values():
            if table.qr_code == qr_code:
                return table
        return None

    # Session methods
    def create_session(self, table_id: UUID, device_id: str, language: Language) -> Optional[Session]:
        table = self.get_table(table_id)
        if not table:
            return None

        session = Session(
            id=uuid4(),
            session_token=str(uuid4()),
            table_id=table_id,
            restaurant_id=table.restaurant_id,
            language=language,
            device_id=device_id
        )
        self.sessions[session.id] = session

        # Create cart for session
        cart = Cart(id=uuid4(), session_id=session.id)
        self.carts[cart.id] = cart

        return session

    def get_session(self, session_id: UUID) -> Optional[Session]:
        return self.sessions.get(session_id)

    # Cart methods
    def get_cart_by_session(self, session_id: UUID) -> Optional[Cart]:
        for cart in self.carts.values():
            if cart.session_id == session_id:
                items = [item for item in self.cart_items.values() if item.cart_id == cart.id]
                for item in items:
                    dish = self.get_dish(item.dish_id)
                    if dish:
                        item.dish = DishResponse(
                            id=dish.id,
                            name=dish.name,
                            description=dish.description,
                            price=dish.price,
                            image_url=dish.image_url,
                            is_available=dish.is_available,
                            allergens=dish.allergens,
                            is_vegetarian=dish.is_vegetarian,
                            is_vegan=dish.is_vegan,
                            preparation_time=dish.preparation_time
                        )
                cart.items = items
                cart.total_amount = sum(item.price * item.quantity for item in items)
                return cart
        return None

    def add_cart_item(self, session_id: UUID, dish_id: UUID, quantity: int, comment: Optional[str] = None) -> Optional[CartItem]:
        cart = self.get_cart_by_session(session_id)
        dish = self.get_dish(dish_id)
        if not cart or not dish:
            return None

        # Check if item already exists
        for item in self.cart_items.values():
            if item.cart_id == cart.id and item.dish_id == dish_id:
                item.quantity += quantity
                if comment:
                    item.comment = comment
                return item

        cart_item = CartItem(
            id=uuid4(),
            cart_id=cart.id,
            dish_id=dish_id,
            quantity=quantity,
            price=dish.price,
            comment=comment
        )
        self.cart_items[cart_item.id] = cart_item
        return cart_item

    def update_cart_item(self, item_id: UUID, quantity: Optional[int] = None, comment: Optional[str] = None) -> Optional[CartItem]:
        item = self.cart_items.get(item_id)
        if not item:
            return None
        if quantity is not None:
            item.quantity = quantity
        if comment is not None:
            item.comment = comment
        return item

    def delete_cart_item(self, item_id: UUID) -> bool:
        if item_id in self.cart_items:
            del self.cart_items[item_id]
            return True
        return False

    # Order methods
    def create_order(self, session_id: UUID, comment: Optional[str] = None) -> Optional[Order]:
        session = self.get_session(session_id)
        cart = self.get_cart_by_session(session_id)
        table = self.get_table(session.table_id) if session else None

        if not session or not cart or not table or not cart.items:
            return None

        order = Order(
            id=uuid4(),
            restaurant_id=session.restaurant_id,
            table_id=session.table_id,
            session_id=session_id,
            table_number=table.table_number,
            total_amount=cart.total_amount,
            comment=comment
        )

        # Copy cart items to order items
        for cart_item in cart.items:
            order_item = OrderItem(
                id=uuid4(),
                order_id=order.id,
                dish_id=cart_item.dish_id,
                quantity=cart_item.quantity,
                price=cart_item.price,
                comment=cart_item.comment,
                dish=cart_item.dish
            )
            self.order_items[order_item.id] = order_item
            order.items.append(order_item)

        self.orders[order.id] = order

        # Clear cart
        items_to_delete = [item_id for item_id, item in self.cart_items.items() if item.cart_id == cart.id]
        for item_id in items_to_delete:
            del self.cart_items[item_id]

        return order

    def get_order(self, order_id: UUID) -> Optional[Order]:
        order = self.orders.get(order_id)
        if order:
            order.items = [item for item in self.order_items.values() if item.order_id == order_id]
            for item in order.items:
                dish = self.get_dish(item.dish_id)
                if dish:
                    item.dish = DishResponse(
                        id=dish.id,
                        name=dish.name,
                        description=dish.description,
                        price=dish.price,
                        image_url=dish.image_url,
                        is_available=dish.is_available,
                        allergens=dish.allergens,
                        is_vegetarian=dish.is_vegetarian,
                        is_vegan=dish.is_vegan,
                        preparation_time=dish.preparation_time
                    )
        return order

    def get_orders(self, status: Optional[OrderStatus] = None, restaurant_id: Optional[UUID] = None) -> List[Order]:
        orders = list(self.orders.values())
        if status:
            orders = [o for o in orders if o.status == status]
        if restaurant_id:
            orders = [o for o in orders if o.restaurant_id == restaurant_id]

        for order in orders:
            order.items = [item for item in self.order_items.values() if item.order_id == order.id]

        return sorted(orders, key=lambda x: x.created_at, reverse=True)

    def update_order_status(self, order_id: UUID, status: OrderStatus) -> Optional[Order]:
        order = self.orders.get(order_id)
        if not order:
            return None
        order.status = status
        order.updated_at = datetime.now()
        return self.get_order(order_id)


# Global database instance
db = Database()
