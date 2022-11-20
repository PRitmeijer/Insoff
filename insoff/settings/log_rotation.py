import logging
import logging.handlers
import os

logging.handlers = logging.handlers

class GroupWriteRotatingFileHandler(logging.handlers.RotatingFileHandler):    
    def _open(self):
        prevumask = os.umask(0o000)
        rtv = logging.handlers.RotatingFileHandler._open(self)
        os.umask(prevumask)
        return rtv