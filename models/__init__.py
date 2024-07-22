from sqlalchemy import String, Integer, ForeignKey, Column, Text, Boolean, DateTime, JSON
from datetime import datetime

from models.base import Base


class TypeORM(Base):
    __tablename__ = "card_types"  # Данная таблица содержит типы карточек заданий
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)  # Название типа задания
    description = Column(String(512))  # Описание типа задания
    color = Column(Text, nullable=False)  # Цвет данного типа задания (любой формат)


class AchievementORM(Base):
    __tablename__ = "achievements"  # Данная таблица содержит достижения
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)  # Название достижения
    description = Column(String(512))  # Описание достижения
    static_image = Column(Text)  # Статическая картинка достижения
    animated_image = Column(Text)  # Анимированная картинка достижения


class CardORM(Base):
    __tablename__ = "cards"  # Данная таблица содержит карточки заданий
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)  # Название карточки задания
    description = Column(String(512))  # Описание карточки задания
    extended_description = Column(String(1024))  # Расширенное описание карточки задания
    created_at = Column(DateTime, nullable=False, default=datetime.now)  # Дата создания карточки задания
    type = Column(Integer, ForeignKey("card_types.id"), nullable=False)  # Тип карточки (привязка к типу карточки)
    rewardPoints = Column(Integer)  # Количество баллов за выполнение задания
    rewardAchievement = Column(Integer, ForeignKey("achievements.id"))  # Id связанной ачивки
    activator = Column(Text, nullable=False)  # Активатор карточки
    progress_type = Column(Integer)  # Тип прогресса карточки


class UserORM(Base):
    __tablename__ = "users"  # Данная таблица содержит пользователей
    id = Column(Integer, primary_key=True)
    external_id = Column(String(512), nullable=False, unique=True)
    achievements_history = Column(JSON, default=[])


class CardProgressORM(Base):
    __tablename__ = "card_progress"  # Данная таблица содержит прогресс выполнения заданий
    id = Column(Integer, primary_key=True)
    card = Column(Integer, ForeignKey("cards.id"), nullable=False)  # Id карточки
    user = Column(Integer, ForeignKey("users.id"), nullable=False)  # Id пользователя (в системе)
    progress = Column(Text, nullable=False)  # Прогресс выполнения
    is_finished = Column(Boolean, nullable=False)  # Завершена ли карточка
    finished_at = Column(DateTime)  # Дата завершения


class OperationTypeORM(Base):
    __tablename__ = "operation_types"  # Данная таблица содержит типы операций
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)  # Название типа операции


class OperationHistoryORM(Base):
    __tablename__ = "operation_history"  # Данная таблица содержит историю операций
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey("users.id"), nullable=False)  # Id пользователя (в системе)
    type = Column(Integer, ForeignKey("operation_types.id"), nullable=False)  # Id типа операции
    data = Column(Text, nullable=False)  # Данные операции
    date = Column(DateTime, nullable=False, default=datetime.now)
