import requests
import os
import json
import time
import datetime


# url = 'https://api.grid-hub.app/v1/latest/GB'
target_zones = ['US-CAISO', 'US-NYISO', 'GB', 'AT', 'NL']
headers = {
    'Authorization': 'Bearer ghk_zAgEDSQDO6E80OSmj4wdBJA2wcXOJgcM',
    'Accept': 'application/json'
}
current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M")
for zone in target_zones:
    url = f"https://api.grid-hub.app/v1/latest/{zone}"

    try:
        print(f"Extract API for fetch electricity for zone {zone}...")
        response = requests.get(url, headers=headers)

        # DEBUGGING! quick look for check status and raw content/data
        print(f"Status code: {response.status_code}")
        print(f"Raw content (Text): {response.text[:200]}")

        if response.status_code == 200:
            # fetch json datas
            data = response.json()

            # destinate data to data/raw (data lake)
            file_name = f"latest_{zone}_{current_time}.json"
            file_path = os.path.join("data", "raw", file_name)

            # Load to data lake
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

            print(f"Successfully to load raw data into {file_path}")

        else:
            print(f"Fail to fetch data. Status code: {response.status_code}")

        time.sleep(1)

    except Exception as e:
        print(f"A network disruption occured: {e}")

