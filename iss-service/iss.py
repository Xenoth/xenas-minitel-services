import requests, json, redis, os

KEY_PREFIX = "ISS"
TIME_OF_LIFE = 6000

URL = "http://api.open-notify.org/iss-now.json"

def add_item(redis_inst, value, ttl):
    key_prefix = KEY_PREFIX

    item_number = redis_inst.incr(f"{key_prefix}:counter")
    key = f"{key_prefix}:item{item_number}"
    redis_inst.set(key, value, ex=ttl)
    print(f"Item added : {key} = {value} (expires is {ttl}s)")

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))

redis_inst = redis.StrictRedis(host=redis_host, port=redis_port)

response = requests.get(URL)
data = response.json()

if data["message"] != "success":
    exit(1)

add_item(redis_inst=redis_inst, value=json.dumps(data), ttl=TIME_OF_LIFE)
exit(0)