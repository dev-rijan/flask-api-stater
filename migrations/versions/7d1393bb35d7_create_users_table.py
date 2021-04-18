from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import expression

"""create_users_table

Revision ID: 7d1393bb35d7
Revises: f6e5f45b16c1
Create Date: 2021-04-18 16:13:19.974721

"""

# revision identifiers, used by Alembic.
# revision = '7d1393bb35d7'
revision = '1df86003b69e'
down_revision = None
# down_revision = 'f6e5f45b16c1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column(
                        'id',
                        sa.Integer,
                        primary_key=True
                    ),
                    sa.Column('is_active',
                              sa.Boolean(),
                              server_default=expression.true(),
                              nullable=False),
                    sa.Column('role',
                              sa.Enum('ROLE_ADMIN', 'ROLE_USER',
                                      name='role_types', native_enum=False),
                              server_default='ROLE_ADMIN', nullable=False),
                    sa.Column('username',
                              sa.String(24),
                              unique=True
                              ),
                    sa.Column('email',
                              sa.String(255),
                              unique=True,
                              nullable=False),
                    sa.Column('password', sa.String(128), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP),
                    sa.Column('updated_at', sa.TIMESTAMP))


def downgrade():
    op.drop_table('users')
