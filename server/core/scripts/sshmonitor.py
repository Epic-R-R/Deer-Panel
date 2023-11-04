import subprocess
import re
import random
from typing import List, Dict


def random_color() -> str:
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


def execute_command(command: str) -> str:
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise RuntimeError(
            f"Command failed with error code {process.returncode}: {stderr.decode('utf-8')}"
        )
    return stdout.decode("utf-8")


def online(ssh_port: str) -> List[Dict[str, str]]:
    duplicate = []
    data = []

    command = f"sudo lsof -i :{ssh_port} -n | grep -v root | grep ESTABLISHED"
    output = execute_command(command)
    online_user_list = re.split(r"\r\n|\n|\r", output)

    for user in online_user_list:
        user = re.sub(r"\s+", " ", user)
        if ":AAAA" in user:
            user_array = user.split(":")
        else:
            user_array = user.split(" ")

        user_ip = None
        if len(user_array) >= 9:
            ip = user_array[8].split("->")[1].split(":")[0]
            user_ip = ip

        color = random_color()
        if len(user_array) >= 3 and user_array[2] not in duplicate:
            color = random_color()
            duplicate.append(user_array[2])

        if (
            len(user_array) >= 3
            and user_array[1]
            and user_array[2] not in ["sshd", "root"]
        ):
            data.append(
                {
                    "username": user_array[2],
                    "color": color,
                    "ip": user_ip,
                    "pid": user_array[1],
                    "protocol": "Direct | TLS | WEBSOCKET",
                }
            )

    return data
