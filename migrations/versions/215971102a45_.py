"""empty message

Revision ID: 215971102a45
Revises: a8a24270111e
Create Date: 2020-06-21 12:17:49.998592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '215971102a45'
down_revision = 'a8a24270111e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('details', sa.String(length=400), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('ticket_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ticket_id'], ['ticket.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ticket_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('details', sa.String(length=500), nullable=True),
    sa.Column('ticket_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ticket_id'], ['ticket.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('ticket', sa.Column('date', sa.DateTime(), nullable=False))
    op.add_column('ticket', sa.Column('description', sa.String(length=120), nullable=False))
    op.add_column('ticket', sa.Column('files', sa.String(length=500), nullable=True))
    op.add_column('ticket', sa.Column('priority', sa.String(length=70), nullable=False))
    op.add_column('ticket', sa.Column('ref_num', sa.Integer(), nullable=False))
    op.add_column('ticket', sa.Column('status', sa.String(length=50), nullable=False))
    op.add_column('ticket', sa.Column('ticket_type', sa.String(length=50), nullable=False))
    op.add_column('ticket', sa.Column('title', sa.String(length=120), nullable=False))
    op.drop_column('ticket', 'ticket_description')
    op.drop_column('ticket', 'ticket_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ticket', sa.Column('ticket_name', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
    op.add_column('ticket', sa.Column('ticket_description', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
    op.drop_column('ticket', 'title')
    op.drop_column('ticket', 'ticket_type')
    op.drop_column('ticket', 'status')
    op.drop_column('ticket', 'ref_num')
    op.drop_column('ticket', 'priority')
    op.drop_column('ticket', 'files')
    op.drop_column('ticket', 'description')
    op.drop_column('ticket', 'date')
    op.drop_table('ticket_history')
    op.drop_table('comment')
    # ### end Alembic commands ###