from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from decouple import config


# Creating engine and session_maker
engine = create_async_engine(
    url=config('PG_LINK'),
    echo=False,
    pool_recycle=3600,
)
async_session = async_sessionmaker(engine, expire_on_commit=False)
