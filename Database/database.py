from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import create_engine, Column, Integer, String, Sequence, Float, Boolean, JSON
from sqlalchemy import select

engine = create_async_engine(
    "sqlite+aiosqlite:///Database/users_data.db"
)
new_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

class User(Base):
    __tablename__ = "users_data"

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    user_id = Column(Integer,default="None")
    first_name = Column(String, default="None")
    softs = Column(JSON, default={})

class HWIDEntry(Base):
    __tablename__ = "hwid_entries"

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    hwid = Column(String, default="None")
    soft = Column(String, default="None")
    user_id = Column(Integer, default="None")

async def add_soft_to_user(user_id, soft_name, soft_data):
    async with new_session() as session:
        query = select(User).where(User.user_id == user_id)

        result = await session.execute(query)
        user = result.scalar_one_or_none()

        new_softs = dict(user.softs)
        new_softs[soft_name] = soft_data
        user.softs = new_softs

        session.add(user)
        await session.commit()

async def add_user_to_main_database(user_id,first_name):
    async with new_session() as session:

        new_user = User(user_id=user_id, first_name=first_name)
        session.add(new_user)

        await session.commit()

        return new_user

async def get_user_from_main_db(user_id):
    async with new_session() as session:
        query = select(User).where(User.user_id == user_id)

        result = await session.execute(query)
        user = result.scalar_one_or_none()

        return user

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)