"""First commmit

Revision ID: f501d24eb7f1
Revises: 
Create Date: 2024-02-18 21:06:35.299634

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
import geoalchemy2.types
from app.models import *


# revision identifiers, used by Alembic.
revision = "f501d24eb7f1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    op.create_table(
        "company",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "position",
            geoalchemy2.types.Geometry(geometry_type="POINT", from_text="ST_GeomFromEWKT", name="geometry"),
            nullable=True,
        ),
        sa.Column("category", sa.Enum("Consulting", "Accelerator", "Startup", name="ecompanycategory"), nullable=True),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("website", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("logo", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # op.create_index('idx_company_position', 'company', ['position'], unique=False, postgresql_using='gist')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("idx_company_position", table_name="company", postgresql_using="gist")
    op.drop_table("company")
    op.execute("DROP EXTENSION IF EXISTS postgis")
    # ### end Alembic commands ###
