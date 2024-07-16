import requests

from api.alerts import API_dispatchAlert
from core.app_settings import LOCAL_STORAGE
from utils.common_variables import BASE_INSULTS_URL, BASE_JOKES_URL
from utils.exception_handler import exception_warning_handler


@exception_warning_handler("api")
def API_fetchInsult() -> str:
    url = LOCAL_STORAGE.insultsURL()
    r = requests.get(url=url)
    if r.status_code != 200:
        API_dispatchAlert(f"{'*' * 99}\nINSULT\n--------\n{url}\n{'-' * 99}\n{str(r.reason)}\n", "error")
        return f"API call to '{BASE_INSULTS_URL}' failed with status code <{r.status_code}>"

    r_json = r.json()
    API_dispatchAlert(f"{'*' * 99}\nINSULT\n--------\n{url}\n{'-' * 99}\n{str(r_json)}\n", "event")
    res = r_json.get("insult")

    if res is None:
        res = "An Error Occurred, see log file."

    return str(res)


@exception_warning_handler("api")
def API_fetchJokes():
    """
    gets the constructed url from the storage and makes the request
    to the provided endpoint
    :return:
    """
    url = LOCAL_STORAGE.jokesURL()
    r = requests.get(url=url)
    if r.status_code != 200:
        API_dispatchAlert(f"{'*' * 99}\nJOKE\n-----\n{url}\n{'-' * 99}\n{str(r.reason)}\n", "error")
        return f"API call to '{BASE_JOKES_URL}' failed with status code <{r.status_code}>"

    r_json = r.json()
    msg = f"{'*' * 99}\nJOKE\n----\n{url}\n{'-' * 99}\n{str(r_json)}\n"

    if r_json['error']:
        API_dispatchAlert(msg, "error")
        return f"{r_json['message']}\n\n{r_json['causedBy']}"

    API_dispatchAlert(msg, "event")

    if r_json['type'] == "single":
        return r_json['joke']

    if r_json['type'] == "twopart":
        return f"{r_json['setup']}\n\n{r_json['delivery']}"


def API_fetchContent() -> str:
    """
    decides what fetch response to send back to the user depending on the settings
    :return:
    """
    mode = LOCAL_STORAGE.opts().get("fetch_mode").value()
    if mode == "jokes":
        return API_fetchJokes()
    elif mode == "insults":
        return API_fetchInsult()
    elif mode == "jokes,insults" or mode == "insults,jokes":

        if LOCAL_STORAGE.pointer == 0:  # jokes
            LOCAL_STORAGE.pointer = 1
            return API_fetchJokes()

        if LOCAL_STORAGE.pointer == 1:  # insults
            LOCAL_STORAGE.pointer = 0
            return API_fetchInsult()

    else:
        return API_fetchJokes()
