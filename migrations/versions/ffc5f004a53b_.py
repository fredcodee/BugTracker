"""empty message

Revision ID: ffc5f004a53b
Revises: 820d6fbb01b5
Create Date: 2020-08-02 22:35:13.950386

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffc5f004a53b'
down_revision = '820d6fbb01b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notification', sa.Column('assigned_dev', sa.String(length=120), nullable=True))
    op.add_column('notification', sa.Column('details', sa.String(length=128), nullable=True))
    op.create_index(op.f('ix_notification_details'), 'notification', ['details'], unique=False)
    op.drop_index('ix_notification_name', table_name='notification')
    op.drop_column('notification', 'name')
    op.drop_column('notification', 'payload_json')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notification', sa.Column('payload_json', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('notification', sa.Column('name', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.create_index('ix_notification_name', 'notification', ['name'], unique=False)
    op.drop_index(op.f('ix_notification_details'), table_name='notification')
    op.drop_column('notification', 'details')
    op.drop_column('notification', 'assigned_dev')
    # ### end Alembic commands ###
