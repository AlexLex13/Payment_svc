from redis_om import get_redis_connection
from main import Product
from config import settings
import time

key = "order_completed"
group = "inventory_group"

redis = get_redis_connection(
    host=settings.redis_host,
    port=settings.redis_port,
    db=1
)

try:
    redis.xgroup_create(key, group)
except:
    print('Group already exists!')

while True:
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)
        if results:
            print(results)
            for result in results:
                obj = result[1][0][1]
                try:
                    product = Product.get(obj["product_id"])
                    product.quantity = product.quantity - int(obj["quantity"])
                    product.save()
                except:
                    redis.xadd("refund_order", obj, '*')
    except Exception as e:
        print(str(e))
    time.sleep(1)
