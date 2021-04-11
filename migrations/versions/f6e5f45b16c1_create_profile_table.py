from alembic import op
import sqlalchemy as sa

"""create_profile_table

Revision ID: f6e5f45b16c1
Revises: 1df86003b69e
Create Date: 2020-08-15 12:02:32.314203

"""

# revision identifiers, used by Alembic.
revision = 'f6e5f45b16c1'
down_revision = '1df86003b69e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('profiles',
                    sa.Column(
                        'id',
                        sa.Integer,
                        sa.ForeignKey('users.id',
                                      onupdate='CASCADE',
                                      ondelete='CASCADE'),
                        index=True,
                        primary_key=True
                    ),
                    sa.Column('name', sa.String(120), nullable=False),
                    sa.Column('name_kana', sa.String(120)),
                    sa.Column('created_at', sa.TIMESTAMP),
                    sa.Column('updated_at', sa.TIMESTAMP))


def downgrade():
    op.drop_table('profiles')
