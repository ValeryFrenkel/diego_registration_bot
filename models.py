from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint
from db import Base

class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    when: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    # Раздельные лимиты: по числу команд и по суммарному числу людей
    teams_capacity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)   # None = без лимита
    people_capacity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # None = без лимита

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    registrations: Mapped[list["Registration"]] = relationship(
        back_populates="game",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

class Registration(Base):
    __tablename__ = "registrations"
    __table_args__ = (
        UniqueConstraint("game_id", "user_id", name="uix_reg_game_user"),
        UniqueConstraint("game_id", "team_name", name="uix_reg_game_team"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    chat_id: Mapped[int] = mapped_column(Integer, nullable=False)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id", ondelete="CASCADE"), nullable=False, index=True)
    team_name: Mapped[str] = mapped_column(String(80), nullable=False)
    players: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(16), default="confirmed", nullable=False)  # confirmed|waitlist
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    game: Mapped["Game"] = relationship(back_populates="registrations")
