import configparser
import datetime
import json
import os
from datetime import date

import requests

# Read from config file
conf = configparser.ConfigParser()
conf.read("../cowin.conf")

DISTRICT = int(conf["District"]["district_code"])
AGE_LIMIT = int(conf["DEFAULT"]["age_limit"])
NUM_DAYS = int(conf["DEFAULT"]["num_days"])

HEADER = {
    "accept": "application/json",
    "Accept-Language": "hi_IN",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56",
}


today = date.today()
consecutive_days = (today + datetime.timedelta(days=delta) for delta in range(NUM_DAYS))


def get_url(date, district=DISTRICT):
    formatted_date = date.strftime("%d-%m-%YYYY")
    return f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={district}&date={formatted_date}"


def get_response(url):
    response = requests.get(url, headers=HEADER)
    return response


def notify(text=""):
    text = f"Vaccines Available!  [Age: {AGE_LIMIT}+]\n{text}"

    with open("cowin-centers.txt", "wt") as f:
        f.writelines(text)

    command = f"kdialog --textbox cowin-centers.txt 840 420"
    os.system(command)


if __name__ == "__main__":
    urls = map(get_url, consecutive_days)
    responses = (get_response(url) for url in urls)

    text = []
    for r in responses:
        centers = json.loads(r.content)["sessions"]

        # if request is succesful and centers is non empty
        if r.status_code == 200 and centers:

            for center in centers:
                if center["min_age_limit"] <= AGE_LIMIT:
                    details = " ".join(
                        [
                            center["date"],
                            "|",
                            center["name"],
                            "|",
                            center["address"],
                            "|",
                            "Rs.",
                            center["fee"],
                            "|",
                            str(center["available_capacity"]),
                            "doses",
                        ]
                    )
                    text.append(details)

    if text:
        notify("\n".join(text))
    else:
        print("Not yet available!")
