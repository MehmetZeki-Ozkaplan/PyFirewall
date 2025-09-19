# PyFirewall
Python + PyQt5 based firewall project created as part of my summer internship. Features packet filtering, logging, rule management, and web blocking.Python + PyQt5 based firewall project created as part of my summer internship. Features packet filtering, logging, rule management, and web blocking.

🛡️ PyFirewall – Windows Firewall Application

A modern and lightweight Windows firewall application — Summer Internship Project

<p align="center"> <img src="https://img.shields.io/badge/Python-3.8+-blue?logo=python" /> <img src="https://img.shields.io/badge/PyQt5-GUI-success?logo=qt" /> <img src="https://img.shields.io/badge/Platform-Windows-lightgrey?logo=windows" /> <img src="https://img.shields.io/badge/Status-Active-brightgreen" /> </p>
📖 Project Overview

This project was developed as part of my summer internship. It is a desktop firewall application designed to:

🔎 Monitor network traffic in real-time

🔒 Apply IP/port-based blocking rules

⚡ Detect potential DDOS attacks

🌐 Easily manage website blocking

The goal is to provide a user-friendly and visually modern tool for monitoring and controlling network activity on Windows systems.

| Feature                        | Description                                                                           |
| ------------------------------ | ------------------------------------------------------------------------------------- |
| 🌐 **Live Traffic Monitoring** | Displays real-time network packets in a table with source, destination, and protocol. |
| 🔒 **Rule Management**         | Add or remove IP/port rules to control network traffic.                               |
| 🚫 **Website Blocking**        | Block specific websites using domain or IP resolution.                                |
| ⚠ **DDOS Detection**           | Identifies suspicious traffic patterns and blacklists offenders.                      |
| 📝 **Logging**                 | Saves all events to `firewall_logs.txt`.                                              |
| 🎨 **Modern Interface**        | Built with PyQt5 and a dark theme for a professional look.                            |


📂 Project Structure
PyFirewall/
├── main.py              # Application entry point
├── firewall_gui.py       # User interface
├── firewall_worker.py    # Network traffic handler
├── logger.py             # Logging module
├── theme.py              # Dark theme configuration
└── requirements.txt      # Dependencies


⚙️ Installation and Setup
1️⃣ Dependencies

This project uses the following third-party libraries:
PyQt5 -> https://pypi.org/project/PyQt5/   ( For the graphical user interface )
pydivert -> https://pypi.org/project/pydivert/ ( For capturing network packets on Windows )

2️⃣ Python Installation

1. Download and install Python 3.8+ from https://www.python.org/
2. During installation, make sure to check “Add Python to PATH.”

3️⃣ Install Required Packages

Clone or download the project:
    git clone https://github.com/<username>/<repo-name>.git
    cd <repo-name>

Install dependencies:
    pip install -r requirements.txt

4️⃣ Running the Application

Run the following command from the project directory:
    python main.py

⚠ IMPORTANT: Run as Administrator

pydivert requires administrator privileges to capture network packets:

- Open Command Prompt or PowerShell by selecting “Run as Administrator.”

- If you are using the compiled .exe version, right-click the file and choose “Run as Administrator.”

- Without administrator rights, the application cannot monitor traffic or apply rules.


5️⃣ Alternative: Standalone Executable (.exe)
To create a standalone executable so users can run the application without installing Python:
    pip install pyinstaller
    pyinstaller --onefile --noconsole main.py

- The .exe file will be generated in the dist folder.
- Remember to run the .exe file as administrator.

🧭 Usage Guide

1. Click Start Firewall → Begin monitoring network traffic.
2. Add Rules → Enter an IP or port to create a blocking rule.
3. Block Websites → Enter a domain name to add it to the blacklist.
4. Monitor Traffic → View source, destination, and protocol information in the table.
5. Stop Firewall → Safely stop all operations.

🖼 Suggested Screenshot Placement
<img width="956" height="624" alt="resim" src="https://github.com/user-attachments/assets/ac864602-81c2-4b4a-b4c4-d49aa4dfe3b7" />


🛠 Developer Notes and Future Plans
- Platform Support: Currently supports Windows only.
- Planned Features:
    🔄 Cross-platform compatibility
    📡 Advanced statistics dashboard
    🧪 Automated testing framework


📜 License
This project was developed for educational and internship purposes. It is not intended for commercial use.


🤝 Contributing
Suggestions, bug reports, and feature requests are welcome!
- Report issues: Use the Issues
- Submit improvements: Open a pull request with your proposed changes.
