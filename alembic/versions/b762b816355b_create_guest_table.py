"""create guest table

Revision ID: b762b816355b
Revises: 
Create Date: 2021-08-12 18:23:52.568876

"""
from alembic import op

from sqlalchemy import Column, String, DateTime, Boolean, BigInteger
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = 'b762b816355b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "guest",
        Column("id", BigInteger, primary_key=True),
        Column("document", String, nullable=False),
        Column("first_name", String, nullable=False),
        Column("last_name", String, nullable=False),
        Column("is_active", Boolean, nullable=False, default=True),
        Column("created_at", DateTime(timezone=True), server_default=func.now()),
        Column("updated_at", DateTime(timezone=True), onupdate=func.now()),
    )


def downgrade():
    op.drop_table("guest")
