from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.router.neo4j_basic import router as neo4j_router_basic
from app.router.nodes import router as nodes_router
from app.router.profiles import router as profiles_router
from app.router.redis_basic import router as redis_router

app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_credentials=True,
                   allow_origins=["*"],
                   allow_methods=["*"],
                   allow_headers=["*"])


@app.get("/")
async def read_root():
    return {"HELLO": "EotV RESTful API Service"}


app.include_router(neo4j_router_basic)
app.include_router(redis_router)
app.include_router(nodes_router)
app.include_router(profiles_router)
