"""Added fields for icon and banner images

Revision ID: 3ff5f3b92a84
Revises: f501d24eb7f1
Create Date: 2024-03-06 20:47:52.987515

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
import geoalchemy2.types
from app.models import *


# revision identifiers, used by Alembic.
revision = "3ff5f3b92a84"
down_revision = "f501d24eb7f1"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('spatial_ref_sys')
    op.add_column("company", sa.Column("icon", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column("company", sa.Column("banner_image", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("company", "banner_image")
    op.drop_column("company", "icon")
    op.create_table(
        "spatial_ref_sys",
        sa.Column("srid", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("auth_name", sa.VARCHAR(length=256), autoincrement=False, nullable=True),
        sa.Column("auth_srid", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("srtext", sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
        sa.Column("proj4text", sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
        sa.CheckConstraint("srid > 0 AND srid <= 998999", name="spatial_ref_sys_srid_check"),
        sa.PrimaryKeyConstraint("srid", name="spatial_ref_sys_pkey"),
    )
    # ### end Alembic commands ###
