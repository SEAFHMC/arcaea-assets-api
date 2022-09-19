import ujson as json
from httpx import AsyncClient
from zipfile import ZipFile
from config import Config
from os import listdir, remove
from shutil import move, copy, rmtree

ROOT = Config.ROOT

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}


class AssetsUpdater:
    @classmethod
    async def download_apk(cls):
        async with AsyncClient(timeout=100, verify=False, headers=headers) as client:
            resp = await client.get(
                "https://webapi.lowiro.com/webapi/serve/static/bin/arcaea/apk"
            )
            with open(ROOT / "version.json", "w", encoding="UTF-8") as f:
                f.write(json.dumps(resp.json(), indent=2))
            download_link = resp.json()["value"]["url"]
            version = resp.json()["value"]["version"]
            with open(ROOT / f"arcaea_{version}.apk", "wb") as f:
                resp = await client.get(download_link)
                for chunk in resp.iter_bytes(1024 * 1024):
                    f.write(chunk)

    @classmethod
    def unzip_apk(cls):
        rmtree(ROOT / "assets", ignore_errors=True)
        with open(ROOT / "version.json", "r", encoding="UTF-8") as f:
            version = json.loads(f.read())["value"]["version"]
        zip_file = ZipFile(ROOT / f"arcaea_{version}.apk")
        for file in zip_file.namelist():
            if file.startswith("assets"):
                zip_file.extract(file, ROOT)
        for song_id in listdir(ROOT / "assets" / "songs"):
            move(
                ROOT / "assets" / "songs" / song_id,
                ROOT / "assets" / "songs" / song_id.removeprefix("dl_"),
            )
        copy(ROOT / "assets" / "char" / "5.png", ROOT / "assets" / "char" / "5u.png")
        copy(
            ROOT / "assets" / "char" / "5_icon.png",
            ROOT / "assets" / "char" / "5u_icon.png",
        )
        zip_file.close()
        remove(ROOT / f"arcaea_{version}.apk")

    @classmethod
    async def update(cls):
        await cls.download_apk()
        cls.unzip_apk()

    @classmethod
    async def check_update(cls):
        with open(ROOT / "version.json", "r", encoding="UTF-8") as f:
            local_version = json.loads(f.read())["value"]["version"]
        async with AsyncClient(timeout=100, verify=False, headers=headers) as client:
            resp = await client.get(
                "https://webapi.lowiro.com/webapi/serve/static/bin/arcaea/apk"
            )
            online_version = resp.json()["value"]["version"]
        return local_version == online_version
