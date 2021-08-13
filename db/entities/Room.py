from sqlalchemy import Column, String, Boolean, Integer

from db.entities import Base


class Room(Base):
    name = Column("name", String, nullable=False)

    capacity = Column("capacity", Integer)

    is_active = Column("is_active", Boolean, nullable=False, default=True)
