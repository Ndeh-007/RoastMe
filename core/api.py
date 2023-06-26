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
