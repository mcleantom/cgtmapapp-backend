from pathlib import Path

from mangum import Mangum

from app.api import create_api
from app.core.config import CGTMapBackendConfig

config_path = Path(__file__).parent / "config.json"
api = create_api(CGTMapBackendConfig.parse_file(config_path))
handler = Mangum(api)
