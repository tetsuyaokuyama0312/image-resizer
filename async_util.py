"""
Utility module for asynchronously running task.
"""
import threading


def submit(task):
    """
    Asynchronously runs task in a background thread.

    :param task: function that is the task to be run
    :return thread that runs task
    """
    th = threading.Thread(target=task, daemon=True)
    th.start()
    return th
