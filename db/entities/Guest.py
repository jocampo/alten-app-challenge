from sqlalchemy import Column, String, Boolean

from db.entities import Base


class Guest(Base):
    document = Column("document", String, nullable=False)

    first_name = Column("first_name", String, nullable=False)

    last_name = Column("last_name", String, nullable=False)

    is_active = Column("is_active", Boolean, nullable=False, default=True)

