from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker

import config
from database import create_async_engine

url = URL.create(
    "postgresql+asyncpg",
    username=config.postgresUSER,
    password=config.postgresPSW,
    host=config.postgresIP,
    database=config.postgresDB,
    port=5432

)

async_engine = create_async_engine(url)
session_maker = async_sessionmaker(async_engine, expire_on_commit=True)