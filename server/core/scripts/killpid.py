import subprocess
from typing import Dict


def kill_pid(pid: str) -> Dict[str, str]:
    try:
        # Kill all processes for the pid
        subprocess.run(
            ["sudo", "kill", "-9", pid],
            check=True,
            stderr=subprocess.PIPE,
            text=True,
        )
        return {"message": "Pid killed successfully."}
    except subprocess.CalledProcessError as e:
        if "No such process" in e.stderr:
            return {"error": f"No such process with PID: {pid}"}
        return {"error": str(e)}
    except Exception as e:
        # Catch any other exceptions
        return {"error": str(e)}
