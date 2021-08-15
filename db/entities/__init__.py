from sqlalchemy.orm import declarative_base

from db.entities.BaseEntity import BaseEntity

Base = declarative_base(cls=BaseEntity)
