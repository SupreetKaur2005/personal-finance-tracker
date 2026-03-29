import logging
import sys
from pythonjsonlogger import jsonlogger

class LoggerSetup:
    @staticmethod
    def setup():
        """Configure JSON logging for production readiness"""
        
        # Console handler with JSON format
        logHandler = logging.StreamHandler(sys.stdout)
        formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s')
        logHandler.setFormatter(formatter)
        
        # Get root logger
        logger = logging.getLogger('api_logger')
        if not logger.handlers:
            logger.addHandler(logHandler)
            logger.setLevel(logging.INFO)
            
        return logger
