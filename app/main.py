import uvicorn
import asyncio

from model.base import *

async def main():
    uvicorn.run("service:app", host="0.0.0.0", port=3100, reload=True)


if __name__ == "__main__":
    asyncio.run(main())