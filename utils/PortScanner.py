import socket
import subprocess
import sys
from datetime import datetime


class PortScanner:

    DEFAULT_SERVER = 'localhost'

    RANGE_START = 1
    RANGE_END = 65535

    def __init__(self):
        self.__opened_ports = []
        self.__index = 0
        self.__cancelled = False

    # def get_opened_ports(self):
    #     list_of_ports = ""
    #     for port in range(self.RANGE_START, self.RANGE_END):
    #         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         result = sock.connect_ex((self.DEFAULT_SERVER, port))
    #         if result == 0:
    #             list_of_ports += "Port {: >5}: 	 Open\n".format(port)
    #         sock.close()
    #     return list_of_ports;

    def is_scan_finished(self):
        """The scan is finished either because it terminated (in a natural way) or because it was cancelled (abnormal
        termination)
        :return:
        True if the scan finished. False otherwise
        """
        return self.__index == self.RANGE_END or self.is_scan_cancelled()

    def is_scan_cancelled(self):
        """
        Tells whether the scan was cancelled or not.
        :return:
        True if hte scan was cancelled. False otherwise
        """
        return self.__cancelled

    def get_progress(self):
        return (100 * self.__index) / (1.0 * self.RANGE_END - self.RANGE_START)

    def scan(self):
        self.__opened_ports.clear()
        self.__index = 0
        for port in range(self.RANGE_START, self.RANGE_END+1):
            if self.is_scan_cancelled():
                break
            self.__index = port
            # print(f"Scanning port {port}...")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((self.DEFAULT_SERVER, port))
            if result == 0:
                self.__opened_ports.append(port)
            sock.close()
        return self.__opened_ports.copy();

    def cancel_scan(self):
        """
        Cancels the scan. This provokes that the scan is immediately stop.
        :return:
        """
        self.__cancelled = True

    def get_opened_ports(self):
        return self.__opened_ports.copy();

    def get_report(self):
        report = ""
        for port in self.__opened_ports:
            report += "Port {: >5}: 	 Open\n".format(port)
        return report
