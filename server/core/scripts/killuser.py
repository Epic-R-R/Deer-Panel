import subprocess
from typing import Dict


def kill_user(username: str) -> Dict[str, str]:
    try:
        # Kill all processes for the user
        subprocess.run(
            ["sudo", "killall", "-u", username],
            check=True,
            stderr=subprocess.PIPE,
            text=True,
        )
        return {"message": "User killed successfully."}
    except subprocess.CalledProcessError as e:
        if "Cannot find user" in e.stderr:
            return {"error": f"Cannot find user: {username}"}
        return {"error": str(e)}
    except Exception as e:
        # Catch any other exceptions
        return {"error": str(e)}
