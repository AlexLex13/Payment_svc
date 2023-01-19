from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
from config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis = get_redis_connection(
    host=settings.redis_host,
    port=settings.redis_port,
    db=1
)


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: str
    status: str

    class Meta:
        database = redis


@app.post('/orders')
async def create_order(request: Request):
    body = await request.json()

