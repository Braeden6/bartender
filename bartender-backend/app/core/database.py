from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, Integer, String
from sqlalchemy.future import select

Base = declarative_base()

# Define the Cocktail class
class Cocktail(Base):
    __tablename__ = 'cocktails'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    bartender = Column(String)
    bar_company = Column(String)
    location = Column(String)
    ingredients = Column(String)
    garnish = Column(String)
    glassware = Column(String)
    preparation = Column(String)
    notes = Column(String)
    description = Column(String)
    drink_embeddings = Column(Vector(1536), nullable=False) 

# Asynchronous engine creation
DATABASE_URL = "postgresql+asyncpg://postgres:mysecretpassword@localhost:5432/main"
async_engine = create_async_engine(DATABASE_URL, echo=False)

# Async sessionmaker
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession
)

# Function to get a new database session
async def get_db_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


