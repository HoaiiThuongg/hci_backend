from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from app.core.config import settings

from app.models.base import Base


config = context.config

config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL.replace("%", "%%"),
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def _is_async_url(url: str) -> bool:
    return any(d in url for d in ("+aiosqlite", "+asyncpg", "+aiomysql", "+aioodbc"))


def run_migrations_online() -> None:
    url = settings.DATABASE_URL

    if _is_async_url(url):
        # Driver async (mặc định dev: sqlite+aiosqlite) → chạy migration qua async engine
        import asyncio

        from sqlalchemy.ext.asyncio import async_engine_from_config

        def do_run_migrations(connection) -> None:
            context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
            with context.begin_transaction():
                context.run_migrations()

        async def run_async() -> None:
            connectable = async_engine_from_config(
                {"sqlalchemy.url": url},
                prefix="sqlalchemy.",
                poolclass=pool.NullPool,
            )
            async with connectable.connect() as connection:
                await connection.run_sync(do_run_migrations)
            await connectable.dispose()

        asyncio.run(run_async())
        return

    from sqlalchemy import create_engine

    connectable = create_engine(
        url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

    connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
