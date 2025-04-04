"""initial

Revision ID: 02d24afcd849
Revises: 
Create Date: 2024-07-09 07:23:51.151235

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '02d24afcd849'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# op.execute("ALTER TYPE roleenum ADD VALUE 'supervisor'")

def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groups',
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_groups_id'), 'groups', ['id'], unique=False)
    op.create_table('users',
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('middle_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('full_name', sa.String(length=150), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=250), nullable=True),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.Column('superuser', sa.Boolean(), nullable=True),
    sa.Column('is_email_verified', sa.Boolean(), nullable=True),
    sa.Column('is_phone_verified', sa.Boolean(), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('otp',
    sa.Column('otp', sa.String(length=6), nullable=False),
    sa.Column('email_or_phone', sa.String(length=50), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_otp_id'), 'otp', ['id'], unique=False)
    op.create_table('user_groups',
    sa.Column('role', sa.Enum('admin', 'sub_admin', 'manager', 'staff', 'member', name='roleenum'), nullable=False),
    sa.Column('add_members', sa.Boolean(), nullable=False),
    sa.Column('view_members', sa.Boolean(), nullable=False),
    sa.Column('remove_members', sa.Boolean(), nullable=False),
    sa.Column('edit_members', sa.Boolean(), nullable=False),
    sa.Column('edit_roles', sa.Boolean(), nullable=False),
    sa.Column('buy_subscription', sa.Boolean(), nullable=False),
    sa.Column('edit_subscription', sa.Boolean(), nullable=False),
    sa.Column('view_subscription', sa.Boolean(), nullable=False),
    sa.Column('edit_group', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_groups_id'), 'user_groups', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_groups_id'), table_name='user_groups')
    op.drop_table('user_groups')
    op.drop_index(op.f('ix_otp_id'), table_name='otp')
    op.drop_table('otp')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_groups_id'), table_name='groups')
    op.drop_table('groups')
    op.execute("DROP TYPE roleenum;")
    # ### end Alembic commands ###
