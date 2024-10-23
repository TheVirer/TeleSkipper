from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import create_engine, Column, Integer, String, Sequence, Float, Boolean
from sqlalchemy import select

engine = create_async_engine(
    "sqlite+aiosqlite:///Bot/BotDatabase/users.db"
)
new_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    user_id = Column(Integer,default="None")
    username = Column(String,default="None")
    first_name = Column(String, default="None")
    reg_data = Column(String)

async def add_user_to_bot_database(user_id,first_name,username,reg_data):
    async with new_session() as session:

        new_user = User(user_id=user_id, username=username, first_name=first_name, reg_data=reg_data)
        session.add(new_user)

        await session.commit()

        return new_user

async def get_user_from_bot_db(user_id):
    async with new_session() as session:
        query = select(User).where(User.user_id == user_id)

        result = await session.execute(query)
        user = result.scalar_one_or_none()

        return user

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)