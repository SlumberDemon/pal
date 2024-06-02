import sys
import threading
import time
from contextlib import contextmanager


@contextmanager
def spinner(text: str):
    def animation(event, text):
        while not event.is_set():
            for cursor in "|/-\\":
                sys.stdout.write(f"\r{cursor} {text}")
                sys.stdout.flush()
                time.sleep(0.1)
            if event.is_set():
                break

    event = threading.Event()
    thread = threading.Thread(target=animation, args=(event, text))
    thread.start()

    try:
        yield
    finally:
        event.set()
        thread.join()
        sys.stdout.write("\r" + " " * (len(text) + 2) + "\r")
