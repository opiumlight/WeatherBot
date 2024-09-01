from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from decouple import config
# noinspection PyUnresolvedReferences
from database.models import Base

# Creating engine and session_maker
engine = create_async_engine(
    url=config('PG_LINK'),
    echo=False,
    pool_recycle=3600,
)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
