from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
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
    db=settings.redis_db
)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get("/products")
async def get_all_products():
    return [Product.get(pk) for pk in Product.all_pks()]


@app.get("/products/{pk}")
async def get_one_product(pk: str):
    return Product.get(pk)


@app.post("/products")
async def create_product(product: Product):
    return product.save()


@app.delete("/products/{pk}")
async def delete_product(pk: str):
    return Product.delete(pk)
