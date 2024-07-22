from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, insert
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from models import *
from schemas.database import *
from config import database_url

router = APIRouter(prefix="/database")

engine = create_async_engine(database_url, echo=True, pool_recycle=3600, pool_pre_ping=True)

async_sessionmaker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

simple_404_responses = {
    404: {"description": "Not found"}
}

simple_404_409_responses = {
    404: {"description": "Not found"},
    409: {"description": "Conflict"}
}


async def get_db():
    async with async_sessionmaker() as session:
        yield session


@router.get("/users", tags=["Users"])
async def get_all_users(db: AsyncSession = Depends(get_db)) -> list[User]:
    all_users = (await db.execute(select(UserORM))).scalars().all()
    return [User.from_orm(user) for user in all_users]


@router.get("/user/{user_id}", responses=simple_404_responses, tags=["Users"])
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)) -> User:
    db_user = (await db.execute(select(UserORM).where(UserORM.id == user_id))).scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return User.from_orm(db_user)


@router.post("/user", responses=simple_404_409_responses, tags=["Users"])
async def create_user(user: User, db: AsyncSession = Depends(get_db)) -> User:
    async with db.begin():
        if (await db.execute(
                select(UserORM).where(UserORM.external_id == user.external_id))).scalar_one_or_none() is not None:
            raise HTTPException(status_code=409, detail=f"User with external_id {user.external_id} already exists")

        user.id = None
        await db.execute(insert(UserORM).values(**user.dict()))

    db_user = (await db.execute(select(UserORM).where(UserORM.external_id == user.external_id))).scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=400, detail=f"Can't create user {user}")
    return User.from_orm(db_user)


@router.delete("/user/{user_id}", responses=simple_404_responses, tags=["Users"])
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)) -> str:
    async with db.begin():
        db_user = (await db.execute(select(UserORM).where(UserORM.id == user_id))).scalar_one_or_none()
        if db_user is None:
            raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

        await db.execute(delete(UserORM).where(UserORM.id == user_id))
    return 'Success'


@router.patch("/user/{user_id}/achievements", tags=["Users"])
async def update_user_achievements(user_id: int, achievements: list[AchievementStatus], db: AsyncSession = Depends(get_db)) -> User:
    async with db.begin():
        db_user = (await db.execute(select(UserORM).where(UserORM.id == user_id))).scalar_one_or_none()
        if db_user is None:
            raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
        db_user.achievements_history =[achievement.dict() for achievement in achievements]
    user = (await db.execute(select(UserORM).where(UserORM.id == user_id))).scalar_one_or_none()
    return User.from_orm(user)


# Achievements
@router.get("/achievements", tags=["Achievements"])
async def get_all_achievements(db: AsyncSession = Depends(get_db)) -> list[Achievement]:
    all_achievements = (await db.execute(select(AchievementORM))).scalars().all()
    return [Achievement.from_orm(achievement) for achievement in all_achievements]


@router.get("/achievement/{achievement_id}", responses=simple_404_responses, tags=["Achievements"])
async def get_achievement_by_id(achievement_id: int, db: AsyncSession = Depends(get_db)) -> Achievement:
    db_achievement = (
        await db.execute(select(AchievementORM).where(AchievementORM.id == achievement_id))).scalar_one_or_none()
    if db_achievement is None:
        raise HTTPException(status_code=404, detail=f"Achievement with id {achievement_id} not found")
    return Achievement.from_orm(db_achievement)
