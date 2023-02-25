"""add user column to posts table

Revision ID: cc3342cb581c
Revises: d191b821dc39
Create Date: 2023-02-24 11:38:14.781599

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc3342cb581c'
down_revision = 'd191b821dc39'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner', sa.String, nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'owner')
    pass
