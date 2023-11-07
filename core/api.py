import requests


def fetchInsult():
    url = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
    r = requests.get(url=url)
    r_json = r.json()
    try:
        r_dict = r_json.get("insult")
        return r_dict
    except Exception as error:
        return error


def fetchJoke():
    url = "https://icanhazdadjoke.com/"
    agent = "My Library (https://github.com/Ndeh-007/RoastMe)"
    header = {"User-Agent": agent, "Accept": "application/json"}
    r = requests.get(url=url, headers=header)
    print(r.content)
    r_json = r.json()
    try:
        r_dict = r_json.get("joke")
        return r_dict
    except Exception as error:
        return error
