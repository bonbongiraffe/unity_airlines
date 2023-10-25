"""revert to integer for timezone and flight time

Revision ID: e6726f4022fa
Revises: ffc5ad15d6c2
Create Date: 2023-10-24 17:53:45.714755

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6726f4022fa'
down_revision = 'ffc5ad15d6c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('flights', schema=None) as batch_op:
        batch_op.alter_column('timezone_change',
               existing_type=sa.DATETIME(),
               type_=sa.Integer(),
               existing_nullable=True)
        batch_op.alter_column('flight_time',
               existing_type=sa.DATETIME(),
               type_=sa.Integer(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('flights', schema=None) as batch_op:
        batch_op.alter_column('flight_time',
               existing_type=sa.Integer(),
               type_=sa.DATETIME(),
               existing_nullable=True)
        batch_op.alter_column('timezone_change',
               existing_type=sa.Integer(),
               type_=sa.DATETIME(),
               existing_nullable=True)

    # ### end Alembic commands ###
