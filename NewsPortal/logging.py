import logging


class LevelDependentFormatter(logging.Formatter):
    default_fmt = "%(asctime)s | %(levelname)s | %(message)s"
    warning_fmt = "%(asctime)s | %(levelname)s | %(message)s | %(pathname)s"
    error_fmt = "%(asctime)s | %(levelname)s | %(message)s | %(pathname)s\n%(exc_text)s"

    def format(self, record):
        if record.levelno >= logging.ERROR:
            self._style._fmt = self.error_fmt
            if record.exc_info and not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        elif record.levelno >= logging.WARNING:
            self._style._fmt = self.warning_fmt
            record.exc_text = None
        else:
            self._style._fmt = self.default_fmt
            record.exc_text = None

        return super().format(record)


class ErrorEmailFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            "fmt",
            "%(asctime)s | %(levelname)s | %(message)s | %(pathname)s"
        )
        super().__init__(*args, **kwargs)