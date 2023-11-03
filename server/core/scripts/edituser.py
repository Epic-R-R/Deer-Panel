import subprocess
from typing import Dict


def manage_user(data: Dict[str, str]) -> Dict[str, str]:
    username = data["username"]
    password = data["password"]
    try:
        if data["activate"] == "active":
            # Create the user and set the password
            subprocess.run(
                [
                    "sudo",
                    "adduser",
                    "--disabled-password",
                    "--gecos",
                    "",
                    "--shell",
                    "/usr/sbin/nologin",
                    username,
                ],
                check=True,
            )
            process = subprocess.Popen(
                ["sudo", "chpasswd"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            process.communicate(input=f"{username}:{password}".encode())
        else:
            subprocess.run(["sudo", "killall", "-u", username])
            subprocess.run(["sudo", "pkill", "-u", username])
            subprocess.run(["sudo", "timeout", "10", "pkill", "-u", username])
            subprocess.run(["sudo", "timeout", "10", "killall", "-u", username])
            subprocess.run(
                ["sudo", "userdel", "-r", username], stderr=subprocess.DEVNULL
            )
            subprocess.run(
                ["sudo", "userdel", "-r", username], stderr=subprocess.DEVNULL
            )

        return {"message": "User management succeeded"}

    except subprocess.CalledProcessError as e:
        return {"message": f"Subprocess error: {e}"}
    except Exception as e:
        return {"message": f"An error occurred: {e}"}
