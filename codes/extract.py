with open("state_id.csv", "rt") as f:
    states = f.readlines()[1:]

import requests
import json

HEADER = {
    "accept": "application/json",
    "Accept-Language": "hi_IN",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56",
}

for state in states:
    head = ['district_id,district_name']
    text = []
    idx, name = state.split(",", 1)
    name = name[:-1]

    url = f'https://cdn-api.co-vin.in/api/v2/admin/location/districts/{idx}'

    response = requests.get(url, headers=HEADER)
    dslist = json.loads(response.content)
    assert(len(dslist)==2)

    for d in dslist["districts"]:
        id_name = d["district_id"],d["district_name"]
        text.append(id_name)

    text = [str(d[0])+","+d[1] for d in sorted(text, key=lambda x: x[-1])]

    content = "\n".join(head+text)
    filename = f'{idx}-{name}.csv'

    with open(filename, "wt") as f:
        f.writelines(content)
