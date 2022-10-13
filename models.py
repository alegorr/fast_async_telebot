from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean
from db import db, metadata

users = Table(
    'users',
    metadata,
    Column("id", Integer, primary_key=True),
    Column("is_bot", Boolean, default=False),
    Column("username", String),
    Column("first_name", String),
    Column("last_name", String),
    Column("language_code", String),
    Column("service_id", Integer, ForeignKey('services.id')),
)

services = Table(
    'services',
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("url", String),
)

transactions = Table(
    'transactions',
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey('users.id')),
    Column("service_id", Integer, ForeignKey('services.id')),
    Column("input", String),
    Column("output", String),
    Column("complete", Boolean, default=False),
    Column("error", String),
)

class User:
    @classmethod
    async def get(cls, id):
        query = users.select().where(users.c.id == id)
        user = await db.fetch_one(query)
        if user:
            return id
        return None

    @classmethod
    async def create(cls, **user):
        query = users.insert().values(**user)
        uid = await db.execute(query)
        return uid

    @classmethod
    async def set_service(cls, user_id, service_id):
        query = users.update().where(users.c.id == user_id).values(service_id=service_id)
        await db.execute(query)

    @classmethod
    async def get_service(cls, uid):
        query = user.select().where(users.c.id == uid)
        user = await db.fetch_one(query)
        if user:
            return user.service_id
        return None

class Service:
    @classmethod
    async def get(cls, id):
        query = services.select().where(services.c.id == id)
        service = await db.fetch_one(query)
        if service:
            return id
        return None

    @classmethod
    async def create(cls, **service):
        print(service)
        query = services.select().where(services.c.url == service['url'])
        service = await db.fetch_one(query)
        if service:
            return None
        query = services.insert().values(**service)
        sid = await db.execute(query)
        return sid

    @classmethod
    async def get_all(cls):
        query = services.select()
        services_list = await db.fetch_all(query)
        return services_list

class Transaction:
    @classmethod
    async def get(cls, id):
        query = transactions.select().where(transactions.c.id == id)
        transaction = await db.fetch_one(query)
        return transaction

    @classmethod
    async def create(cls, **transaction):
        query = transactions.insert().values(**transaction)
        tid = await db.execute(query)
        return tid

    @classmethod
    async def get_all(cls):
        query = transactions.select()
        transactions_list = await db.fetch_all(query)
        return transactions_list

    @classmethod
    async def update(cls, tid, **transaction):
        query = transactions.update().where(transactions.c.id == tid).values(**transaction)
        await db.execute(query)
