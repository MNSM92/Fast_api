"""add user table

Revision ID: 864598b2e13e
Revises: cc3342cb581c
Create Date: 2023-02-24 12:39:19.700117

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision = '864598b2e13e'
down_revision = 'cc3342cb581c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('email', sa.String, nullable=False, unique=True),
                    sa.Column('password', sa.String, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
