from alembic import op
import sqlalchemy as sa

from lib.util_datetime import tzware_datetime
from lib.util_sqlalchemy import AwareDateTime


"""create_revoked_tokens_table

Revision ID: 10c6de1fdacb
Revises: 
Create Date: 2020-08-09 20:58:00.835884

"""

# revision identifiers, used by Alembic.
revision = '1df86003b69e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('revoked_tokens',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('jti', sa.String(120), unique=True, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP),
                    sa.Column('updated_at', sa.TIMESTAMP))


def downgrade():
    op.drop_table('revoked_tokens')