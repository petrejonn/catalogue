"""empty message

Revision ID: eb5c01544c0f
Revises: 358373f7dec6
Create Date: 2024-01-29 22:55:22.875235

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "eb5c01544c0f"
down_revision = "358373f7dec6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("categories", sa.Column("created_at", sa.DateTime(), nullable=False))
    op.add_column("categories", sa.Column("updated_at", sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("categories", "updated_at")
    op.drop_column("categories", "created_at")
    # ### end Alembic commands ###