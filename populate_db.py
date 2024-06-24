from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# Создание всех таблиц
models.Base.metadata.create_all(bind=engine)

# Функция для заполнения базы данных
def populate_db():
    db: Session = SessionLocal()

    # Добавление пользователей
    user1 = models.User(first_name="John", last_name="Doe", email="john.doe@example.com", password="secret")
    user2 = models.User(first_name="Jane", last_name="Smith", email="jane.smith@example.com", password="secret")
    db.add(user1)
    db.add(user2)

    # Добавление продуктов
    product1 = models.Product(name="Product1", description="Description1", price=100.0)
    product2 = models.Product(name="Product2", description="Description2", price=200.0)
    db.add(product1)
    db.add(product2)

    # Добавление заказов
    order1 = models.Order(user_id=1, product_id=1, order_date=datetime.now(), order_status="Pending")
    order2 = models.Order(user_id=2, product_id=2, order_date=datetime.now(), order_status="Shipped")
    db.add(order1)
    db.add(order2)

    # Сохранение изменений
    db.commit()
    db.close()

if __name__ == "__main__":
    populate_db()

