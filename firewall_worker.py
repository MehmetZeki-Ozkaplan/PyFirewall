from PyQt5.QtCore import QThread, pyqtSignal
from collections import defaultdict
import time
import socket
import pydivert

from core.logger import log_to_file

class FirewallWorker(QThread):
    log_signal = pyqtSignal(str, str, str)
    rules_signal = pyqtSignal(str)

    PROTOCOL_MAP = {
        1: "ICMP", 2: "IGMP", 6: "TCP", 8: "EGP", 9: "IGP", 17: "UDP",
        41: "IPv6", 50: "ESP", 51: "AH", 58: "ICMPv6", 89: "OSPF",
        112: "VRRP", 132: "SCTP", 137: "MPLS-in-IP", 143: "EtherIP", 255: "Experimental (Reserved)"
    }

    def __init__(self, rules, website_filter):
        super().__init__()
        self.rules = rules
        self.website_filter = website_filter
        self.running = True
        self.traffic_tracker = defaultdict(list)
        self.blacklist = set()
        self.whitelist = {"127.0.0.1", "::1"}

    @staticmethod
    def resolve_url_to_ip(url):
        try:
            return socket.gethostbyname(url)
        except socket.gaierror:
            return None

    def get_protocol_name(self, protocol):
        if isinstance(protocol, tuple):
            protocol = protocol[0]
        return self.PROTOCOL_MAP.get(protocol, f"Bilinmiyor ({protocol})")

    def run(self):
        try:
            with pydivert.WinDivert("tcp or udp") as w:
                for packet in w:
                    if not self.running:
                        break

                    src_ip = packet.src_addr
                    dst_ip = packet.dst_addr
                    protocol = self.get_protocol_name(packet.protocol)
                    current_time = time.time()

                    if src_ip in self.whitelist:
                        w.send(packet)
                        continue

                    if src_ip in self.blacklist:
                        self.rules_signal.emit(f"IP kara listede: {src_ip}")
                        continue

                    if dst_ip in self.website_filter:
                        self.rules_signal.emit(f"Engellendi: {dst_ip} (Web Sitesi)")
                        continue

                    self.traffic_tracker[src_ip].append(current_time)
                    short_window = [ts for ts in self.traffic_tracker[src_ip] if current_time - ts <= 1]
                    long_window = [ts for ts in self.traffic_tracker[src_ip] if current_time - ts <= 10]

                    if len(short_window) > 10000 or len(long_window) > 50000:
                        self.rules_signal.emit(
                            f"DDOS Saldırısı Tespit Edildi: {src_ip} (1s: {len(short_window)}, 10s: {len(long_window)})"
                        )
                        self.blacklist.add(src_ip)
                        log_to_file(f"DDOS tespit edildi ve engellendi: {src_ip}", "warning")
                        continue

                    self.log_signal.emit(src_ip, dst_ip, protocol)
                    log_to_file(f"Paket: {src_ip}:{packet.src_port} -> {dst_ip}:{packet.dst_port}")

                    blocked = False
                    for rule in self.rules:
                        if "tcp" in rule.lower() and protocol.lower() == "tcp":
                            self.rules_signal.emit("TCP paketi engellendi")
                            blocked = True
                            break
                        elif "udp" in rule.lower() and protocol.lower() == "udp":
                            self.rules_signal.emit("UDP paketi engellendi")
                            blocked = True
                            break
                        elif rule in f"{packet.src_addr}:{packet.src_port}" or rule in f"{packet.dst_addr}:{packet.dst_port}":
                            self.rules_signal.emit(f"Paket engellendi: {rule}")
                            log_to_file(f"Kural engellendi: {rule}", "warning")
                            blocked = True
                            break

                    if not blocked:
                        w.send(packet)
        except Exception as e:
            self.rules_signal.emit(f"Hata: {str(e)}")
            log_to_file(f"Hata: {str(e)}", "error")

    def stop(self):
        self.running = False
