import logging
import signal
from functools import partial

from fastapi import FastAPI


def _handler_termination_signal(signum, frame, app: FastAPI) -> None:
    logging.info("Received SIGTERM signal, mark service to unhealthy.")
    app.state.stop_event.set()

def init_app(app: FastAPI) -> None:
    signal.signal(signal.SIGTERM, partial(_handler_termination_signal, app=app))
    signal.signal(signal.SIGINT, partial(_handler_termination_signal, app=app))
