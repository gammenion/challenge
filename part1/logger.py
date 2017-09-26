""" logger.py

    Abstraction for the logging layer
    
    This code is licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)
"""
from datetime import datetime
import socket

class Logger():
    """The Logger class implements an extensible method for logging"""

    def __init__(self):
        """Initialization of Logger class

        Args:
            None

        Sets:
            self.format (str): the format string of the printable message
        """
        self.format = "{time} - {ip} - {msg}"

    def log(self, msg):
        """For now, this method only logs to stdout
        
        Args:
            msg (str): A string representing what to log

        Returns:
            No value

        Prints:
            Prints to screen in the format: date - IP/Host - message
                Example: 2017-09-01 - localhost - Message to be printed
        """
        log = {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                "ip": socket.getfqdn(), 
                "msg":msg
            }
        print self.format.format(**log)

