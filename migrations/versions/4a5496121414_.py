"""empty message

Revision ID: 4a5496121414
Revises: ffc5f004a53b
Create Date: 2020-08-03 02:06:11.653354

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4a5496121414'
down_revision = 'ffc5f004a53b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notification', sa.Column('date', sa.DateTime(), nullable=True))
    op.add_column('notification', sa.Column('link', sa.String(length=128), nullable=True))
    op.drop_index('ix_notification_timestamp', table_name='notification')
    op.drop_column('notification', 'timestamp')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notification', sa.Column('timestamp', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.create_index('ix_notification_timestamp', 'notification', ['timestamp'], unique=False)
    op.drop_column('notification', 'link')
    op.drop_column('notification', 'date')
    # ### end Alembic commands ###
