"""change timezone change and flight time to interval column types

Revision ID: ffc5ad15d6c2
Revises: e56e6e323a2e
Create Date: 2023-10-24 17:19:51.381976

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffc5ad15d6c2'
down_revision = 'e56e6e323a2e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('flights', schema=None) as batch_op:
        batch_op.alter_column('timezone_change',
               existing_type=sa.INTEGER(),
               type_=sa.Interval(),
               existing_nullable=True)
        batch_op.alter_column('flight_time',
               existing_type=sa.TIME(),
               type_=sa.Interval(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('flights', schema=None) as batch_op:
        batch_op.alter_column('flight_time',
               existing_type=sa.Interval(),
               type_=sa.TIME(),
               existing_nullable=True)
        batch_op.alter_column('timezone_change',
               existing_type=sa.Interval(),
               type_=sa.INTEGER(),
               existing_nullable=True)

    # ### end Alembic commands ###