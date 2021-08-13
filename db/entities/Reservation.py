from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, BigInteger, Integer, Enum

from db.entities import Base


class Reservation(Base):
    Column("room_id", BigInteger,
           ForeignKey('room.id', name="fk_room_id", onupdate="RESTRICT", ondelete="RESTRICT"), nullable=False),
    Column("guest_id", BigInteger,
           ForeignKey('guest.id', name="fk_guest_id", onupdate="RESTRICT", ondelete="RESTRICT"), nullable=False),
    Column("start_date", DateTime(timezone=True), nullable=False),
    Column("end_date", DateTime(timezone=True), nullable=False),
    Column("amount_of_guests", Integer),
    Column("status", Enum("SCHEDULED", " CANCELED", name="reservation_status_type"), nullable=False, default="SCHEDULED"),
