"""add foreign key to posts table

Revision ID: 997333e9dc40
Revises: 864598b2e13e
Create Date: 2023-02-24 12:55:02.019397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '997333e9dc40'
down_revision = '864598b2e13e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key('post_fk', source_table='posts', referent_table='users',
                          local_cols= ['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('post_fk', table_name='posts')
    op.drop_column('posts', column_name='owner_id')
    pass
