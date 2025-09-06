import logging
import sys


def setup_logging(service_name: str):
    formatter = logging.Formatter(
        fmt=f"%(asctime)s | {service_name} | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)  # default
    root_logger.handlers.clear()  # avoid duplicate logs
    root_logger.addHandler(handler)

    # Tune FastAPI/uvicorn loggers too
    logging.getLogger("uvicorn").handlers.clear()
    logging.getLogger("uvicorn.error").handlers.clear()
    logging.getLogger("uvicorn.access").handlers.clear()

    logging.getLogger("uvicorn").addHandler(handler)
    logging.getLogger("uvicorn.error").addHandler(handler)
    logging.getLogger("uvicorn.access").addHandler(handler)

    return root_logger
