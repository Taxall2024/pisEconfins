import logging

import coloredlogs


class Logger:

    def init_log(self):
        console_format = "%(levelname)s: %(message)s"

        # console config
        log = logging.getLogger('log')
        coloredlogs.install(logger=log, fmt=console_format)

        return log