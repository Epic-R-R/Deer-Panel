<div align="center">
<h1 align="center">
<img src="https://gcdnb.pbrd.co/images/iZDzHQjZf7lf.png?o=1" width="100" />
<br>DEER PANEL</h1>
<h3>◦ SSH User Management.</h3>
<h3>◦ Developed with the software and tools below.</h3>

<p align="center">
<img src="https://img.shields.io/badge/GNU%20Bash-4EAA25.svg?style=flat-square&logo=GNU-Bash&logoColor=white" alt="GNU%20Bash" />
<img src="https://img.shields.io/badge/.ENV-ECD53F.svg?style=flat-square&logo=dotenv&logoColor=black" alt=".ENV" />
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat-square&logo=Python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/Django-092E20.svg?style=flat-square&logo=Django&logoColor=white" alt="Django" />
</p>
<img src="https://img.shields.io/github/license/Epic-R-R/Deer-Panel?style=flat-square&color=5D6D7E" alt="GitHub license" />
<img src="https://img.shields.io/github/last-commit/Epic-R-R/Deer-Panel?style=flat-square&color=5D6D7E" alt="git-last-commit" />
<img src="https://img.shields.io/github/commit-activity/m/Epic-R-R/Deer-Panel?style=flat-square&color=5D6D7E" alt="GitHub commit activity" />
<img src="https://img.shields.io/github/languages/top/Epic-R-R/Deer-Panel?style=flat-square&color=5D6D7E" alt="GitHub top language" />
</div>

---

##  Table of Contents
- [ Table of Contents](#-table-of-contents)
- [ Overview](#-overview)
- [ Features](#-features)
- [ repository Structure](#-repository-structure)
- [ Modules](#modules)
- [ Getting Started](#-getting-started)
    - [ Installation](#-installation)
    - [ Running Deer-Panel](#-running-Deer-Panel)
    - [ Tests](#-tests)
- [ Roadmap](#-roadmap)
- [ Contributing](#-contributing)
- [ License](#-license)
- [ Acknowledgments](#-acknowledgments)

---


##  Overview

**Deer Panel**, a Django-driven venture, serves as a potent and adaptable platform for overseeing users and their network interactions. Encapsulated within are extensive APIs tailored for user administration, traffic scrutiny, and server configuration management. Accompanying these are a curated set of scripts facilitating user account lifecycle management, server health monitoring, and traffic filtration.

## Highlighted Features:

- **User Management:** Seamless user account creation, modification, and deletion. Features include activation/deactivation toggles and comprehensive traffic monitoring per user.
- **Traffic Monitoring:** Real-time tracking of upload, download, and aggregate traffic metrics on a per-user basis.
- **Server Settings:** Effortless management of SSH and TLS ports, language preferences, and multi-user status configurations.
- **Scripts Suite:** A collection of scripts dedicated to user and server administration, ensuring smooth operations.

Under the hood, Deer Panel leverages the capabilities of Django alongside the Django Rest Framework for backend operations, with a MySQL database anchoring data storage needs. The code architecture is meticulously crafted, housing a robust suite of tests to uphold software quality and reliability standards.

##  Repository Structure

```sh
└── server/
      └── core/
         ├── api/
         ├── core/
         ├── install.sh
         ├── manage.py
         ├── requirements.txt
         └── scripts/
├── .gitignore
├── LICENSE
├── README.md
└── install.sh
```

---


##  Modules

<details closed><summary>Core</summary>

| File                                                                                                  | Summary                   |
| ---                                                                                                   | ---                       |
| [manage.py](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/manage.py)               | The **manage.py** script in Deer Panel serves as a command-line interface for handling administrative tasks in Django, setting the default settings module to **core.settings** and allowing the execution of management commands. |
| [requirements.txt](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/requirements.txt) | The **requirements.txt** file in Deer Panel lists the necessary Python packages for the project, ensuring all dependencies are known and can be installed for proper functionality. |
| [install.sh](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/install.sh)             | The **install.sh** script in Deer Panel automates the setup of sudo privileges for specified or current users. It prompts for a username, creates temporary sudoers configurations, validates them with **visudo**, then appends them to the system's sudoers file, ensuring safe and streamlined privilege escalation setup. |
| [settings.py](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/core/settings.py)      | The **settings.py** file in Deer Panel configures Django project settings, defining the setup for databases, apps, middleware, and other key components crucial for the project's functionality. |
| [.env](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/core/.env)                    | The **.env** file in Deer Panel holds environment variables crucial for configuring aspects like database connections, secret keys, and other settings, keeping sensitive data separate from the codebase for better security and flexibility. |
| [urls.py](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/core/urls.py)              | In Deer Panel, the **urls.py** file under core defines URL patterns, routing requests to the Django admin interface and to the API endpoints as specified in **api.urls**, thus orchestrating the project's web routing. |
| [asgi.py](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/core/asgi.py)              | The script configures ASGI for Deer Panel's core, enabling asynchronous communication between the web server and application with **core.settings** as the default module. |
| [wsgi.py](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/core/wsgi.py)              | The script configures WSGI for Deer Panel's core, setting up synchronous communication between the web server and application, with **core.settings** as the default module. |

</details>

<details closed><summary>Scripts</summary>

| File                                                                                                            | Summary                   |
| ---                                                                                                             | ---                       |
| [sshmonitor.py](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/scripts/sshmonitor.py)         | The script in Deer Panel executes a shell command to identify online users on a specified SSH port, extracting their IP addresses and process IDs, while filtering out certain user types. |
| [edituser.py](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/scripts/edituser.py)             | The **edituser** function in Deer Panel facilitates user modification, managing SSH configurations and error handling, while providing operation status feedbac |
| [createuser.py](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/scripts/createuser.py)         | The script in Deer Panel orchestrates user creation, modifies SSH configuration for active users, and handles errors, returning operation status messages. |
| [killuser.py](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/scripts/killuser.py)             | The **kill_user** function in Deer Panel terminates all processes for a specified user, handling errors to provide a success or error message. |
| [deleteuser.py](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/scripts/deleteuser.py)         | The **delete_user** function in Deer Panel eradicates a specified user's processes, updates SSH configuration, removes the user's banner, and deletes the user from the system, handling any exceptions to provide a success or error message. |
| [status.py](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/scripts/status.py)                 | The script in Deer Panel gathers system information including operating system details, processor specifications, and RAM usage, organizing and returning this data in a structured dictionary for further utilization. |
| [filteringcheck.py](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/scripts/filteringcheck.py) | The **filtering** function in Deer Panel fetches the server's IP, checks its connectivity from various locations, filters the results based on predefined flags, and returns a list of dictionaries containing the status, IP, and location of each check, with a specific focus on allowed geographic regions. |
| [killpid.py](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/scripts/killpid.py)               | The **kill_pid** function in Deer Panel terminates a process based on its PID, handling errors to provide a success or error message regarding the operation's outcome. |

</details>

<details closed><summary>Api</summary>

| File                                                                                                  | Summary                   |
| ---                                                                                                   | ---                       |
| [tests.py](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/api/tests.py)             | The **tests.py** file in Deer Panel contains the suite of tests that verify the functionality and correctness of the application's components, ensuring the reliability and robustness of the software as it evolves. |
| [views.py](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/api/views.py)             | The **views.py** file in Deer Panel houses the logic for handling requests and rendering responses, orchestrating data retrieval and processing to deliver the appropriate content or actions based on user interactions. |
| [token.py](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/api/token.py)             | The **token.py** file in Deer Panel is responsible for generating access and refresh tokens, which are crucial for managing user sessions and ensuring secure and authorized interactions within the application. |
| [models.py](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/api/models.py)           | The **models.py** file in Deer Panel defines the data models and relationships, serving as the blueprint for the database schema and facilitating the ORM layer for data interaction. |
| [apps.py](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/api/apps.py)               | The **apps.py** file in Deer Panel configures the Django application settings, facilitating the setup and customization of app components and behaviors to align with project requirements |
| [admin.py](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/api/admin.py)             | Registers **Client, Traffic, and Settings** models for Django's admin interface. |
| [urls.py](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/api/urls.py)               | The **urls.py** file within the API app of Deer Panel maps URLs to the corresponding view functions specific to the API, facilitating the routing and handling of HTTP requests to deliver data and services in a structured format. |
| [serializers.py](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/api/serializers.py) | The **serializer.py** file in Deer Panel translates complex data types into a format that can be easily rendered into JSON, XML, or other content types. It also provides deserialization, converting parsed data back into complex types, aiding in the validation and transformation of data between the application and the client. |

</details>

<details closed><summary>Commands</summary>

| File                                                                                                                              | Summary                   |
| ---                                                                                                                               | ---                       |
| [cronexp_traffic.py](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/api/management/commands/cronexp_traffic.py) | **TODO WRITE SUMMARY FOR IT.** |
| [synstraffics.py](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/api/management/commands/synstraffics.py)       | **TODO WRITE SUMMARY FOR IT.** |
| [cronexp.py](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/api/management/commands/cronexp.py)                 | **TODO WRITE SUMMARY FOR IT.** |
| [multiuser.py](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/api/management/commands/multiuser.py)             | The **multiuser** command in Deer Panel monitors the number of active connections per user against their defined limitations. It iterates through the currently connected users, updating their usage records, and disconnects users exceeding their allowed simultaneous connections. |

</details>

<details closed><summary>Migrations</summary>

| File                                                                                                               | Summary                   |
| ---                                                                                                                | ---                       |
| [0001_initial.py](https://github.com/Epic-R-R/Deer-Panel/blob/main/server/core/api/migrations/0001_initial.py) | The **0001_initial.py** file in Django contains the instructions for creating the initial database schema for an app based on the current state of its models. |

</details>

---

##  Getting Started

***Dependencies***

Please ensure you have the following dependencies installed on your system:

###  Installation

1. Clone the Deer-Panel repository:
```sh
git clone https://github.com/Epic-R-R/Deer-Panel.git
```

2. Change to the project directory:
```sh
cd Deer-Panel/server/core
```

3. Install the dependencies:
```sh
pip install -r requirements.txt
```

###  Running Deer-Panel

```sh
python manage.py runserver
```

###  Tests
```sh
python manage.py test
```

---


##  Project Roadmap

> - [X] `ℹ️  Task 1: User and Server Management Implementation`
> - [ ] `ℹ️  Task 2: Scheduled Traffic and User Management Implementation`
> - [ ] `ℹ️ ...`


---

##  Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Submit Pull Requests](https://github.com/Epic-R-R/Deer-Panel)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/Epic-R-R/Deer-Panel/discussions)**: Share your insights, provide feedback, or ask questions.
- **[Report Issues](https://github.com/Epic-R-R/Deer-Panel/issues)**: Submit bugs found or log feature requests for EPIC-R-R.

#### *Contributing Guidelines*

<details closed>
<summary>Click to expand</summary>

1. **Fork the Repository**: Start by forking the project repository to your GitHub account.
2. **Clone Locally**: Clone the forked repository to your local machine using a Git client.
   ```sh
   git clone <your-forked-repo-url>
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear and concise message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to GitHub**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.

Once your PR is reviewed and approved, it will be merged into the main branch.

</details>

---

##  License

This project is protected under the [MIT License](https://choosealicense.com/licenses/mit/). For more details, refer to the [LICENSE](https://github.com/Epic-R-R/Deer-Panel/blob/master/LICENSE) file.

---

[**Return to top**](#Top)
