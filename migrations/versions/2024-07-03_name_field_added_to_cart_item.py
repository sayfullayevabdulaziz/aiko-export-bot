"""name field added to cart_item

Revision ID: 387c7a1657f7
Revises: c7a04958c744
Create Date: 2024-07-03 07:11:58.503884

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '387c7a1657f7'
down_revision: Union[str, None] = 'c7a04958c744'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart_item', sa.Column('name', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cart_item', 'name')    
    # ### end Alembic commands ###
