import asyncio
import logging
from typing import Any
from sqlalchemy import (
    Double,
    Integer,
    Sequence,
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
    UniqueConstraint,
    create_engine,
)

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio import async_sessionmaker


class Base(DeclarativeBase):
    pass


class Update(Base):
    __tablename__ = "test"
    __table_args__ = (PrimaryKeyConstraint("id", name="update_pkey"),)
    id: Mapped[int] = mapped_column(Integer, Sequence("test_id_seq"), primary_key=True)
    value: Mapped[float] = mapped_column(Double(53))

    data1: Mapped["Data1"] = relationship(
        "Data1", uselist=False, back_populates="update"
    )


class Data1(Base):
    __tablename__ = "data1"
    __table_args__ = (
        ForeignKeyConstraint(
            ["update_id"],
            ["test.id"],
            deferrable=True,
            initially="DEFERRED",
            name="fk_data1",
        ),
        PrimaryKeyConstraint("id", name="data1_pkey"),
        UniqueConstraint(
            "update_id",
            name="data1_update_id_key",
        ),
    )
    id: Mapped[int] = mapped_column(Integer, Sequence("data1_id_seq"), primary_key=True)
    data1: Mapped[float] = mapped_column(Double(53))

    update_id: Mapped[int] = mapped_column(Integer)
    update: Mapped["Update"] = relationship("Update", back_populates="data1")


def handle_exception(loop: asyncio.AbstractEventLoop, context: dict[Any, Any]) -> None:
    msg = context.get("exception", context["message"])
    logging.error(
        f"This should not happen: Caught unhandled exception: {msg} {context}"
    )


async def main():
    logging.basicConfig(level=logging.DEBUG)

    logging.info("Start")

    loop = asyncio.get_event_loop()
    loop.set_exception_handler(handle_exception)

    sync_engine = create_engine(
        f"postgresql+psycopg://test:test@testdb:5432/test",
        echo=True,
        pool_size=2,
    )
    Base.metadata.create_all(sync_engine)

    engine: AsyncEngine = create_async_engine(
        f"postgresql+psycopg://test:test@testdb:5432/test",
        echo=True,
        pool_size=2,
    )

    async_session = async_sessionmaker(engine)
    for _ in range(10):
        async with async_session() as session:
            logging.info("Add batch")
            for _ in range(4):
                update = Update(value=8.5514716)
                session.add(update)
            await session.commit()
            await asyncio.sleep(5)


asyncio.run(main())
