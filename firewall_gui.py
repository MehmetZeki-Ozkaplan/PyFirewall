from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QLineEdit,
    QListWidget, QTextEdit, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QIcon
from core.firewall_worker import FirewallWorker

class FirewallGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Firewall")
        self.setWindowIcon(QIcon("iconfire.ico"))

        screen = self.screen()
        screen_size = screen.size()
        self.resize(screen_size.width() // 2, screen_size.height() // 2)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.rules = []
        self.website_filter = set()
        self.firewall_worker = None

        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout()

        self.start_button = QPushButton("Start Firewall")
        self.start_button.clicked.connect(self.start_firewall)
        self.stop_button = QPushButton("Stop Firewall")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_firewall)

        rule_layout = QHBoxLayout()
        self.rule_input = QLineEdit()
        self.rule_input.setPlaceholderText("Enter rule (exp. 192.168.1.1:80)")
        self.add_rule_button = QPushButton("Add Rule")
        self.add_rule_button.clicked.connect(self.add_rule)
        rule_layout.addWidget(self.rule_input)
        rule_layout.addWidget(self.add_rule_button)

        self.rule_list = QListWidget()
        self.delete_rule_button = QPushButton("Delete Selected Rule")
        self.delete_rule_button.clicked.connect(self.delete_rule)

        self.log_area = QTableWidget()
        self.log_area.setColumnCount(3)
        self.log_area.setHorizontalHeaderLabels(["Source", "Target", "Protocol"])
        self.log_area.setEditTriggers(QTableWidget.NoEditTriggers)
        self.log_area.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.rules_area = QTextEdit()
        self.rules_area.setReadOnly(True)

        self.web_list = QListWidget()
        website_layout = QHBoxLayout()
        self.website_input = QLineEdit()
        self.website_input.setPlaceholderText("Site to be blocked (exp. www.site.com)")
        self.add_website_button = QPushButton("Add")
        self.add_website_button.clicked.connect(self.add_website)
        website_layout.addWidget(self.website_input)
        website_layout.addWidget(self.add_website_button)

        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(QLabel("Rules:"))
        layout.addWidget(self.rule_list)
        layout.addLayout(rule_layout)
        layout.addWidget(self.delete_rule_button)
        layout.addWidget(QLabel("Network Traffic:"))
        layout.addWidget(self.log_area)
        layout.addWidget(QLabel("Applied Rules:"))
        layout.addWidget(self.rules_area)
        layout.addWidget(QLabel("Blocked Sites:"))
        layout.addWidget(self.web_list)
        layout.addLayout(website_layout)

        self.main_widget.setLayout(layout)

    def add_to_traffic_table(self, src, dst, protocol):
        row = self.log_area.rowCount()
        self.log_area.insertRow(row)
        self.log_area.setItem(row, 0, QTableWidgetItem(src))
        self.log_area.setItem(row, 1, QTableWidgetItem(dst))
        self.log_area.setItem(row, 2, QTableWidgetItem(protocol))

    def add_rule(self):
        rule = self.rule_input.text().strip()
        if rule:
            self.rules.append(rule)
            self.rule_list.addItem(rule)
            self.rules_area.append(f"Rule added: {rule}")
            self.rule_input.clear()
        else:
            QMessageBox.warning(self, "Warning", "Enter a valid rule!")

    def delete_rule(self):
        item = self.rule_list.currentItem()
        if item:
            rule = item.text()
            self.rules.remove(rule)
            self.rule_list.takeItem(self.rule_list.row(item))
            self.rules_area.append(f"Rule deleted: {rule}")
        else:
            QMessageBox.warning(self, "Warning", "Select a rule to delete!")

    def add_website(self):
        url = self.website_input.text().strip()
        if url and self.firewall_worker:
            ip = self.firewall_worker.resolve_url_to_ip(url)
            if ip:
                self.website_filter.add(ip)
                self.web_list.addItem(f"{url} ({ip})")
                self.rules_area.append(f"The website is blocked: {url} ({ip})")
                self.website_input.clear()
            else:
                QMessageBox.warning(self, "Warning", "Enter a valid URL!")
        else:
            QMessageBox.warning(self, "Warning", "Enter a URL!")

    def start_firewall(self):
        if not self.firewall_worker:
            self.firewall_worker = FirewallWorker(self.rules, self.website_filter)
            self.firewall_worker.log_signal.connect(self.add_to_traffic_table)
            self.firewall_worker.rules_signal.connect(self.rules_area.append)
            self.firewall_worker.start()
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)

    def stop_firewall(self):
        if self.firewall_worker:
            self.firewall_worker.stop()
            self.firewall_worker.quit()
            self.firewall_worker.wait()
            self.firewall_worker = None
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.rules_area.append("Firewall stopped.")
