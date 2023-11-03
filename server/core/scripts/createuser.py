import subprocess
from typing import Dict


def create_user(data: Dict[str, str]) -> Dict[str, str]:
    try:
        # Modify sshd_config file
        if data["status"] == "active":
            replacement = (
                f"Match User {data['username']}\\n"
                f"Banner /var/www/html/app/storage/banner/{data['username']}-detail\\n"
                "Match all"
            )
            command = (
                f"sudo sed -i 's@#Match all@{replacement}@' /etc/ssh/sshd_config && "
                "sudo service ssh restart"
            )

            process = subprocess.Popen(command, shell=True)
            process.communicate()

        subprocess.run(
            [
                "sudo",
                "adduser",
                "--disabled-password",
                "--gecos",
                "",
                "--shell",
                "/usr/sbin/nologin",
                data["username"],
            ],
            check=True,
        )
        process = subprocess.Popen(
            ["sudo", "chpasswd"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        process.communicate(input=f"{data['username']}:{data['password']}".encode())

        return {"message": "User created successfully"}

    except subprocess.CalledProcessError as e:
        return {"message": f"Subprocess error: {e}"}
    except Exception as e:
        return {"message": f"An error occurred: {e}"}
