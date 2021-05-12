import configparser
import datetime
import json
import os
from datetime import date

import asyncio
import aiohttp

# Read from config file
conf = configparser.ConfigParser()
conf.read("../cowin.conf")

DISTRICT = int(conf["District"]["district_code"])
AGE_LIMIT = int(conf["DEFAULT"]["age_limit"])
NUM_DAYS = int(conf["DEFAULT"]["num_days"])

HEADERS = {
    "accept": "application/json",
    "Accept-Language": "hi_IN",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56",
}


today = date.today()
consecutive_days = (today + datetime.timedelta(days=delta) for delta in range(NUM_DAYS))


def get_url(date, district=DISTRICT):
    formatted_date = date.strftime("%d-%m-%YYYY")
    return f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={district}&date={formatted_date}"

url_list = [get_url(date) for date in consecutive_days]

async def fetch(session, url):
    async with session.get(url, headers=HEADERS) as response:
        return await response.json()

async def fetch_all(urls, loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(*[fetch(session, url) for url in urls], return_exceptions=True)
        return results

def notify(text=""):
    text = f"Vaccines Available!  [Age: {AGE_LIMIT}+]\n{text}"

    with open("cowin-centers.txt", "wt") as f:
        f.writelines(text)

    command = f"kdialog --textbox cowin-centers.txt 840 420"
    os.system(command)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    urls = url_list
    responses = loop.run_until_complete(fetch_all(urls, loop))

    text = []

    for r in responses:

        centers = r["sessions"]

        # if centers is non empty
        if centers:

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
