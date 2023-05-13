from apscheduler.schedulers.asyncio import AsyncIOScheduler
from assets_updater import AssetsUpdater

scheduler = AsyncIOScheduler()


@scheduler.scheduled_job("interval", hours=8)
async def _():
    if await AssetsUpdater.check_update():
        await AssetsUpdater.update()
