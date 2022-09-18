from pathlib import Path


class Config:
    token = "616.sb"
    base_url = None
    ROOT = Path("/etc/nginx/arcaea")


Config.ROOT.mkdir(parents=True, exist_ok=True)
