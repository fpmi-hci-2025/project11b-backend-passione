# Passione Backend

REST API сервер для системы управления рестораном Passione. Построен на FastAPI с in-memory базой данных.

## Требования

- Python 3.10+
- pip

## Установка

```bash
cd project11b-backend-passione
pip install -r requirements.txt
```

## Запуск

```bash
uvicorn app.main:app --reload --port 8000
```

Сервер запустится на http://localhost:8000

## API Документация

После запуска доступна интерактивная документация:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Структура проекта

```
app/
├── main.py           # Точка входа, конфигурация FastAPI
├── models.py         # Pydantic модели данных
├── database.py       # In-memory база с демо-данными
└── routers/
    ├── restaurants.py  # Эндпоинты ресторанов и меню
    ├── sessions.py     # Управление сессиями клиентов
    ├── carts.py        # Корзина покупок
    ├── orders.py       # Заказы и их статусы
    └── dishes.py       # Управление блюдами
```

## API Эндпоинты

### Меню
- `GET /api/restaurants/{id}/menu?lang=ru` - получить меню ресторана

### Сессии
- `POST /api/sessions` - создать сессию клиента

### Корзина
- `GET /api/carts/{session_id}` - получить корзину
- `POST /api/carts/{session_id}/items` - добавить блюдо в корзину
- `PATCH /api/cart-items/{item_id}` - изменить количество
- `DELETE /api/cart-items/{item_id}` - удалить из корзины

### Заказы
- `POST /api/orders` - создать заказ
- `GET /api/orders` - список всех заказов
- `GET /api/orders/{id}/status` - статус заказа
- `PATCH /api/orders/{id}/status` - изменить статус заказа

### Блюда (админ)
- `GET /api/dishes` - список всех блюд
- `PATCH /api/dishes/{id}` - редактировать блюдо

## Статусы заказов

Workflow статусов:
```
PENDING -> CONFIRMED -> PREPARING -> READY -> DELIVERED
                                          \-> CANCELLED
```

## Демо-данные

При запуске автоматически создаются:
- 1 ресторан (ID: 11111111-1111-1111-1111-111111111111)
- 2 столика
- 5 категорий меню
- 12 блюд с изображениями

## CORS

Разрешены запросы с любых origins для разработки.

## Примеры запросов

Создать сессию:
```bash
curl -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{"table_id": "33333333-3333-3333-3333-333333333331", "device_id": "test", "language": "ru"}'
```

Получить меню:
```bash
curl http://localhost:8000/api/restaurants/11111111-1111-1111-1111-111111111111/menu?lang=ru
```

Добавить в корзину:
```bash
curl -X POST http://localhost:8000/api/carts/{session_id}/items \
  -H "Content-Type: application/json" \
  -d '{"dish_id": "55555555-5555-5555-5555-555555555501", "quantity": 2}'
```
