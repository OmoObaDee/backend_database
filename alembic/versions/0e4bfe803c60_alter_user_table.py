"""alter user table

Revision ID: 0e4bfe803c60
Revises: 
Create Date: 2025-10-23 11:58:02.693542

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e4bfe803c60'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# def upgrade() -> None:
#     """Upgrade schema."""
#     pass


# def downgrade() -> None:
#     """Downgrade schema."""
#     pass

def upgrade() -> None:
    op.execute("""
    ALTER TABLE user
    ADD COLUMN userType varchar(100)
""")
    pass
def downgrade() -> None:
    op.execute("""
    ALTER TABLE user
    DROP COLUMN userType
""")
    pass