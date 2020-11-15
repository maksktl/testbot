from typing import List

import sqlalchemy as sa
from aiogram import Dispatcher
from gino import Gino
from gino.schema import GinoSchemaVisitor
from sqlalchemy import Column, DateTime

from data.config import POSTGRES_USER, POSTGRES_PASSWORD, PG_HOST, POSTGRES_DB

db = Gino()


class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


async def on_startup(dispatcher: Dispatcher):
    await db.set_bind(f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{PG_HOST}/{POSTGRES_DB}')

    # Create tables
    db.gino: GinoSchemaVisitor
    # await db.gino.drop_all()  # Drop the db
    await db.gino.create_all()
