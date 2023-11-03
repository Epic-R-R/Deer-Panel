from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Client, Settings
import subprocess
import json


class Command(BaseCommand):
    help = "Manage multiuser functionality"

    def handle(self, *args, **kwargs):
        settings = Settings.load()
        multiuser_status = settings.status_multiuser

        if multiuser_status == "active":
            command = f"sudo lsof -i :{settings.ssh_port} -n | grep -v root | grep ESTABLISHED"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            output, _ = process.communicate()
            online_user_list = output.decode().strip().split("\n")
            online_list = []
            for user in online_user_list:
                user_array = user.split()
                username = user_array[2] if len(user_array) > 2 else None
                online_list.append(username)

            # json_file_path = "/var/www/html/app/storage/dropbear.json"
            # status = subprocess.call(f"test -e '{json_file_path}'", shell=True)
            # if json_file_path:
            #     with open(json_file_path, "r") as file:
            #         data_array = json.load(file)
            #         for item in data_array:
            #             user = item.get("user")
            #             online_list.append(user)

            online_list = [user for user in online_list if user]
            online_count = {user: online_list.count(user) for user in online_list}

            for username in online_count:
                self.stdout.write(self.style.SUCCESS(f"Processing user: {username}"))
                clients = Client.objects.filter(username=username)
                for client in clients:
                    limitation = client.multiuser
                    start_date = client.start_date
                    finish_date_one_connect = client.date_one_connect
                    # Assuming the date fields are in 'YYYY-MM-DD' format
                    if not start_date:
                        if online_count[username] > 0:
                            start_inp = timezone.now().strftime("%Y-%m-%d")
                            end_inp = (
                                timezone.now()
                                + timezone.timedelta(days=int(finish_date_one_connect))
                            ).strftime("%Y-%m-%d")
                            client.start_date = start_inp
                            client.end_date = end_inp
                            client.save()

                    if limitation != 0 and online_count[username] > limitation:
                        # if status:
                        #     with open(json_file_path, "r") as file:
                        #         data_array = json.load(file)
                        #         for item in data_array:
                        #             if item.get("user") == username:
                        #                 pid = item["PID"]
                        #                 subprocess.run(
                        #                     f"sudo kill -9 {pid}", shell=True
                        #                 )
                        # Kill all processes for the user and delete the user from the system
                        subprocess.run(["sudo", "killall", "-u", username])
                        subprocess.run(["sudo", "pkill", "-u", username])
                        subprocess.run(
                            ["sudo", "timeout", "10", "pkill", "-u", username]
                        )
                        subprocess.run(
                            ["sudo", "timeout", "10", "killall", "-u", username]
                        )
