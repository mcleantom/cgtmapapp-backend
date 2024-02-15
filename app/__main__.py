import click
import uvicorn

from app.core.config import CGTMapBackendConfig
from app.api import create_api
from app.models import init, destruct


@click.group()
def main():
    pass


@main.command("run")
@click.option("--config", type=click.Path(exists=True), help="Path to the config file")
@click.option("--port", default=5000, help="Port to run the server on")
@click.option("--host", default="localhost", help="Host to run the server on")
def run(config: str, port: int, host: str):
    config = CGTMapBackendConfig.parse_file(config)
    api = create_api(config)
    uvicorn.run(api, host=host, port=port)


@main.command("init")
def init_db():
    init()


@main.command("destruct")
def destruct_db():
    destruct()


if __name__ == "__main__":
    main()
