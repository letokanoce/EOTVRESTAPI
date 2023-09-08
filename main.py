import asyncio

import uvicorn

from app.configuration.configs import CommonSettings

common_settings = CommonSettings()


async def main():
    uvicorn.run("app.service:app", host=common_settings.HOST, port=common_settings.PORT, reload=True)


if __name__ == "__main__":
    asyncio.run(main())
