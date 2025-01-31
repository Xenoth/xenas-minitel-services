import requests, os, redis, json, datetime
from bs4 import BeautifulSoup

URL = "https://calendhaiiku.com/"

TIME_OF_LIFE = 1209600

KEY_HAIKUS = "HAIKUS"

redis_host = os.getenv("REDIS_HOST", "cache")
redis_port = int(os.getenv("REDIS_PORT", 6379))

redis_inst = redis.StrictRedis(host=redis_host, port=redis_port)

response = requests.get(URL)

current_date = datetime.datetime.today().strftime("%Y-%m-%d")

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    haikus = []

    for haiku_block in soup.find_all('li', class_='haiiku'):
        haiku_data = {}

        date_span = haiku_block.find('span', {'data-date': True})
        haiku_date = date_span['data-date'] if date_span else None
        if current_date != haiku_date:
            print(str(current_date) + '!=' + str(haiku_date))
            continue

        haiku_data['date'] = haiku_date

        cite_tags = haiku_block.find_all('cite')
        if cite_tags:
            haiku_data['text'] = "\n".join([cite.get_text() for cite in cite_tags])
        else:
            haiku_data['text'] = None

        link = haiku_block.find('a', href=True)
        haiku_data['url'] = link['href'] if link else None

        author_div = haiku_block.find('div', class_='display-name-vig')
        haiku_data['author'] = author_div['data-user_nicename'] if author_div else None

        haikus.append(haiku_data)

    for i, haiku in enumerate(haikus, 1):
        print(f"Haïku {i}:")
        print(f"  Texte :\n{haiku['text']}")
        print(f"  Date : {haiku['date']}")
        print(f"  URL : {haiku['url']}")
        print(f"  Auteur : {haiku['author']}")
        print("-" * 40)

    redis_inst.set(KEY_HAIKUS, json.dumps(haikus))