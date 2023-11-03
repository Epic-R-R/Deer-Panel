import requests
import time
import re
from typing import List, Dict


def filtering() -> List[Dict[str, str]]:
    data = []
    server_ip = requests.get("http://myip.dnsomatic.com").content.decode("utf-8")
    # url = f"https://check-host.net/check-tcp?host={server_ip}:{PORT_SSH}&max_nodes=50"
    url = f"https://check-host.net/check-tcp?host={server_ip}:22&max_nodes=50"
    headers = {"Accept": "application/json", "Cache-Control": "no-cache"}
    response = requests.post(url, headers=headers)
    array = response.json()
    result_link = f"https://check-host.net/check-result/{array['request_id']}"
    time.sleep(3)
    server_output = requests.post(result_link, headers=headers)
    array2 = server_output.json()
    allowed_flags = ["ir", "us", "fr", "de"]
    data = []

    for key, value in array2.items():
        flag = re.sub(r".node.check-host.net", "", key)
        flag = re.sub(r"[0-9]+", "", flag)
        if flag in allowed_flags:
            url = "https://check-host.net/nodes/hosts"
            response = requests.get(url)
            ip_add = ""
            location = ""
            if response.status_code == 200:
                json_data = response.json()
                search_key = key
                if search_key in json_data["nodes"]:
                    location = json_data["nodes"][search_key]["location"]
                    ip_add = json_data["nodes"][search_key]["ip"]

            status = "Filter" if value is None else "Online"
            data.append(
                {"flag": flag, "status": status, "ip": ip_add, "location": location}
            )

    return data
