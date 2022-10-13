from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
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
        return user

    @classmethod
    async def create(cls, **user):
        query = users.insert().values(**user)
        uid = await db.execute(query)
        return uid

class Service:
    @classmethod
    async def get(cls, id):
        query = services.select().where(services.c.id == id)
        service = await db.fetch_one(query)
        return service

    @classmethod
    async def create(cls, **service):
        query = services.insert().values(**service)
        sid = await db.execute(query)
        return sid

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
