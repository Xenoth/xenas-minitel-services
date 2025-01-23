import requests, time, redis, os, json

KEY_CAMPAIGNS = "HELLDIVERS-CAMPAIGNS"
KEY_ASSIGNMENTS = "HELLDIVERS-ASSIGNMENTS"

TIME_OF_LIFE = 1209600

URL_CAMPAIGNS = "https://api.helldivers2.dev/api/v1/campaigns"
URL_ASSIGNMENTS = "https://api.helldivers2.dev/api/v1/assignments"

redis_host = os.getenv("REDIS_HOST", "cache")
redis_port = int(os.getenv("REDIS_PORT", 6379))

redis_inst = redis.StrictRedis(host=redis_host, port=redis_port)

retry = True
while(retry):
    try:
        response = requests.get(URL_CAMPAIGNS, headers={'X-Super-Client': 'minitel.xenoth.fr', 'X-Super-Contact': 'xenothvalack@gmail.com'})
        response.raise_for_status()
        data = response.json()
        
        redis_inst.set(KEY_CAMPAIGNS, json.dumps(data))
        retry = False
    except requests.exceptions.RequestException as e:
        if response.status_code == 429:
            retry_time = int(response.headers['retry-after'])
            time.sleep(int(response.headers['retry-after']))
        else:
            exit(1)

retry = True
while(retry):
    try:
        response = requests.get(URL_ASSIGNMENTS, headers={'X-Super-Client': 'minitel.xenoth.fr', 'X-Super-Contact': 'xenothvalack@gmail.com'})
        response.raise_for_status()
        data = response.json()

        redis_inst.set(KEY_ASSIGNMENTS, json.dumps(data))
        retry = False
    except requests.exceptions.RequestException as e:
        if response.status_code == 429:
            retry_time = int(response.headers['retry-after'])
            time.sleep(int(response.headers['retry-after']))
        else:
            exit(1)

exit(0)