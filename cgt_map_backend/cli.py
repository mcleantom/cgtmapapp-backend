import click
import uvicorn
from .config import CGTMapBackendConfig, MongoDBConfig
from .app import create_app


@click.group()
def main():
    pass


@main.command("run")
@click.option("--config", type=click.Path(exists=True), help="Path to the config file")
@click.option("--port", default=5000, help="Port to run the server on")
@click.option("--host", default="0.0.0.0", help="Host to run the server on")
def run(
    config: str,
    port: int,
    host: str
):
    config = CGTMapBackendConfig.parse_file(config)
    app = create_app(config)
    uvicorn.run(app, host=host, port=port)
