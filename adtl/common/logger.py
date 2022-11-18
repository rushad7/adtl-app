import logging


class ADTLLogger:
    __shared_instance = None

    def __init__(self):
        if ADTLLogger.__shared_instance is not None:
            raise Exception("Can only instantiate Logger class once")
        else:
            ADTLLogger.__shared_instance = self
            self.logger = logging.getLogger("aistudio_log")
            self.logger.setLevel(logging.INFO)
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s [%(levelname)s] %(message)s",
                handlers=[
                    logging.FileHandler("adtl_log.log"),
                    logging.StreamHandler()
                ]
            )

    @staticmethod
    def get_instance():
        if ADTLLogger.__shared_instance is None:
            ADTLLogger()
        return ADTLLogger.__shared_instance

    def close_handlers(self):
        handlers = self.logger.handlers
        for handler in handlers:
            self.logger.removeHandler(handler)
            handler.close()

    def info(self, message: str):
        self.logger.info(message)
        self.close_handlers()

    def warning(self, message: str):
        self.logger.warning(message)
        self.close_handlers()

    def error(self, message: str):
        self.logger.error(message)
        self.close_handlers()
