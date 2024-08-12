import sys
from datetime import datetime


class Logger:
    log = open('../.log', 'a')

    @classmethod
    def debug(cls, msg: str) -> None:
        t = datetime.now().strftime('%Y/%m/%d - %H:%M:%S')
        cls.log.write(f'[DBG] {t} => {msg}')

    def info(self, msg: str) -> None:
        t = datetime.now().strftime('%Y/%m/%d - %H:%M:%S')
        self.log.write(f'[INF] {t} => {msg}')

    def warning(self, msg: str) -> None:
        t = datetime.now().strftime('%Y/%m/%d - %H:%M:%S')
        self.log.write(f'[WAR] {t} => {msg}')

    def error(self, msg: str) -> None:
        t = datetime.now().strftime('%Y/%m/%d - %H:%M:%S')
        self.log.write(f'[ERR] {t} => {msg}')

    def fatal(self, msg: str) -> None:
        t = datetime.now().strftime('%Y/%m/%d - %H:%M:%S')
        self.log.write(f' --- [FATAL ERROR] --- \n{t}\n => {msg}\nThe application will be stopped.')
        sys.exit(1)
