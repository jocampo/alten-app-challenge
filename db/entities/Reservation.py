from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, BigInteger, Integer, Enum

from db.entities import Base


class Reservation(Base):
    room_id = Column("room_id",
                     BigInteger,
                     ForeignKey(
                         'room.id',
                         name="fk_room_id",
                         onupdate="RESTRICT",
                         ondelete="RESTRICT"),
                     nullable=False)

    guest_id = Column("guest_id",
                      BigInteger,
                      ForeignKey(
                          'guest.id',
                          name="fk_guest_id",
                          onupdate="RESTRICT",
                          ondelete="RESTRICT"),
                      nullable=False)

    start_date = Column("start_date", DateTime(timezone=True), nullable=False)

    end_date = Column("end_date", DateTime(timezone=True), nullable=False)

    amount_of_guests = Column("amount_of_guests", Integer)

    status = Column("status",
                    Enum(
                        "SCHEDULED",
                        " CANCELED",
                        name="reservation_status_type"),
                    nullable=False,
                    default="SCHEDULED")
