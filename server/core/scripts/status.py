import subprocess
import os
from typing import Dict, Union


def get_os_info() -> Dict[str, Dict[str, str]]:
    os_info = {}
    with open("/etc/lsb-release", "r") as file:
        for line in file:
            key, value = line.strip().split("=")
            os_info[key] = value

    uname_output = (
        subprocess.run(["uname", "-s", "-r"], capture_output=True, text=True)
        .stdout.strip()
        .split()
    )
    os_info["Kernel"], os_info["Kernel Release"] = uname_output
    # os_info["Derived from OS"] = "Unknown"

    if os.path.exists("/etc/os-release"):
        with open("/etc/os-release", "r") as file:
            for line in file:
                if "LIKE" in line:
                    key, value = line.strip().split("=")
                    os_info["Derived from OS"] = value.replace('"', "")

    return {"OPERATING SYSTEM": os_info}


def get_processor_info() -> Dict[str, Dict[str, str]]:
    processor_info = {}
    with open("/proc/cpuinfo", "r") as file:
        for line in file:
            if line.startswith("model name"):
                processor_info["Model"] = line.strip().split(": ")[1]
            if line.startswith("cache size"):
                processor_info["Cache memory"] = line.strip().split(": ")[1]

    processor_info["CPU cores"] = str(
        len(
            subprocess.run(["lscpu", "-p=cpu"], capture_output=True, text=True)
            .stdout.strip()
            .split("\n")
        )
    )
    processor_info["Architecture"] = subprocess.run(
        ["uname", "-p"], capture_output=True, text=True
    ).stdout.strip()
    processor_usage = subprocess.run(
        [
            "top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\\([0-9.]*\\)%* id.*/\\1/' | awk '{print 100 - $1\"%\"}'"
        ],
        shell=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    processor_info["usage"] = processor_usage

    return {"PROCESSOR": processor_info}


def get_ram_info() -> Dict[str, Dict[str, str]]:
    ram_info = {}
    free_output = (
        subprocess.run(["free", "-m"], capture_output=True, text=True)
        .stdout.split("\n")[1]
        .split()
    )
    total, used, free = map(int, free_output[1:4])
    ram_info["Total"] = f"{total}Mb"
    ram_info["In Use"] = f"{used}Mb"
    ram_info["Free"] = f"{free}Mb"
    ram_info["usage"] = f"{(used/total)*100:.2f}%"

    return {"RAM MEMORY": ram_info}


def main() -> Dict[str, Dict[str, Union[str, Dict[str, str]]]]:
    system_info = {}
    system_info.update(get_os_info())
    system_info.update(get_processor_info())
    system_info.update(get_ram_info())

    return system_info
