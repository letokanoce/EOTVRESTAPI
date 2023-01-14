from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.profiles import router as ProfileRouter
from router.nodes import router as NodeRouter

app = FastAPI(openapi_url="/api/v1/openapi.json")

origins = [
    "http://localhost:3000",
]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(ProfileRouter)
app.include_router(NodeRouter)


@app.get("/root")
async def read_root():
    return {"Hello": "EOTVREST"}


@app.get("/endpoints")
async def get_all_endpoints():
    return [{"path": route.path, "name": route.name} for route in app.routes]
