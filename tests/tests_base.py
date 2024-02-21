from unittest import TestCase

import testing.postgresql

import alembic.config


class TestBase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.postgresql = testing.postgresql.Postgresql()
        cls.conn = cls.postgresql.get_connection()
        cls.engine = cls.postgresql.engine
        cls.metadata.bind = cls.engine
        alembic.config.main(argb=["--raiseerr", "upgrade", "head"])

    @classmethod
    def tearDownClass(cls) -> None:
        cls.conn.close()
        cls.postgresql.stop()

    def test_foo(self):
        pass
