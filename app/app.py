from cgt_map_backend.app import create_app
from cgt_map_backend.config import CGTMapBackendConfig
from pathlib import Path
from mangum import Mangum

config_path = Path(__file__).parent / "config.json"
app = create_app(CGTMapBackendConfig.parse_file(config_path))
handler = Mangum(app)