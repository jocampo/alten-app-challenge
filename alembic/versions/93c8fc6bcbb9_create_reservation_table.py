"""create reservation table

Revision ID: 93c8fc6bcbb9
Revises: 77666aed8f77
Create Date: 2021-08-12 18:48:21.733326

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger, ForeignKey
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = '93c8fc6bcbb9'
down_revision = '77666aed8f77'
branch_labels = None
depends_on = None

reservation_status_type_name = "reservation_status_type"
reservation_status_type = sa.Enum("SCHEDULED", "CANCELED", name=reservation_status_type_name)


def upgrade():
    op.create_table(
        "reservation",
        Column("id", BigInteger, primary_key=True),
        Column("room_id", BigInteger,
               ForeignKey('room.id', name="fk_room_id", onupdate="RESTRICT", ondelete="RESTRICT"), nullable=False),
        Column("guest_id", BigInteger,
               ForeignKey('guest.id', name="fk_guest_id", onupdate="RESTRICT", ondelete="RESTRICT"), nullable=False),
        Column("start_date", DateTime(timezone=True), nullable=False),
        Column("end_date", DateTime(timezone=True), nullable=False),
        Column("amount_of_guests", Integer),
        Column("status", reservation_status_type, nullable=False, default="SCHEDULED"),
        Column("created_at", DateTime(timezone=True), server_default=func.now()),
        Column("updated_at", DateTime(timezone=True), onupdate=func.now()),
    )


def downgrade():
    op.drop_table("reservation")
    with op.get_context().autocommit_block():
        op.execute(f"DROP TYPE {reservation_status_type_name}")
