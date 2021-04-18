from alembic import op
import sqlalchemy as sa


"""create_revoked_tokens_table

Revision ID: 10c6de1fdacb
Revises: 
Create Date: 2020-08-09 20:58:00.835884

"""

# revision identifiers, used by Alembic.
revision = '7d1393bb35d7'
down_revision = 'f6e5f45b16c1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('revoked_tokens',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('jti', sa.String(120),
                              unique=True, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP),
                    sa.Column('updated_at', sa.TIMESTAMP))


def downgrade():
    op.drop_table('revoked_tokens')
