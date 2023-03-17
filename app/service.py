from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router.profiles import router as profile_router
from app.router.nodes import router as node_router
from app.router.cache import router as cache_router

app = FastAPI(openapi_url="/api/v1/openapi.json")

origins = [
    "http://localhost:3000",
]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


@app.get("/root")
async def read_root():
    return {"Hello": "EOTVREST"}


@app.get("/endpoints")
async def get_all_endpoints():
    return [{"path": route.path, "name": route.name} for route in app.routes]


app.include_router(node_router)
app.include_router(profile_router)
app.include_router(cache_router)
