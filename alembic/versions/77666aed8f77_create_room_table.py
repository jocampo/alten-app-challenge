"""create room table

Revision ID: 77666aed8f77
Revises: b762b816355b
Create Date: 2021-08-12 18:42:08.168456

"""
from alembic import op
from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = '77666aed8f77'
down_revision = 'b762b816355b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "room",
        Column("id", BigInteger, primary_key=True),
        Column("name", String, nullable=False),
        Column("capacity", Integer),
        Column("is_active", Boolean, nullable=False, default=True),
        Column("created_at", DateTime(timezone=True), server_default=func.now()),
        Column("updated_at", DateTime(timezone=True), onupdate=func.now()),
    )


def downgrade():
    op.drop_table("room")
