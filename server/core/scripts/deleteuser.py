import subprocess
import tempfile

from typing import Dict


def delete_user(username: str) -> Dict[str, str]:
    try:
        # If the user has an associated banner, remove it
        banner_path = f"/var/www/html/app/storage/banner/{username}-detail"
        status = subprocess.call(f"test -e '{banner_path}'", shell=True)
        if status:
            subprocess.run(["sudo", "rm", "-rf", banner_path])
        # Update the sshd_config file
        ssh_config_path = "/etc/ssh/sshd_config"
        lines_to_remove = [
            f"Match User {username}",
            f"Banner /var/www/html/app/storage/banner/{username}-detail",
        ]

        # Create a temporary file to store the modified configuration
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
            with open(ssh_config_path, "r") as file:
                for line in file:
                    if not any(removal in line for removal in lines_to_remove):
                        temp_file.write(line)
            temp_filename = temp_file.name

        # Move the temporary file to replace sshd_config
        subprocess.run(f"sudo mv {temp_filename} {ssh_config_path}", shell=True)

        # Restart the ssh service
        subprocess.run(["sudo", "service", "ssh", "restart"])

        # Kill all processes for the user and delete the user from the system
        subprocess.run(["sudo", "killall", "-u", username])
        subprocess.run(["sudo", "pkill", "-u", username])
        subprocess.run(["sudo", "timeout", "10", "pkill", "-u", username])
        subprocess.run(["sudo", "timeout", "10", "killall", "-u", username])
        subprocess.run(["sudo", "userdel", "-r", username], stderr=subprocess.DEVNULL)

        return {"message": "User deleted successfully."}

    except Exception as e:
        return {"error": str(e)}
