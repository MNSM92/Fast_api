"""create posts table

Revision ID: d191b821dc39
Revises: 
Create Date: 2023-02-24 10:46:40.057209

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision = 'd191b821dc39'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',
                    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('title', sa.String, nullable=False),
                    sa.Column('content', sa.String, nullable=False),
                    sa.Column('published', sa.Boolean, server_default='TRUE', nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')),
                    sa.Column('owner_id', sa.Integer, nullable=False)
                    #relationship('owner', "User")
                    )
    pass


def downgrade():
    op.drop_table('posts')
    pass
