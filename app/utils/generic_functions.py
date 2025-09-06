import logging
import time

logger = logging.getLogger(__name__)


def execute_with_retries(func, *args, max_retries=3, delay=2, **kwargs):
    """Execute a function with retries on failure.

    Args:
        func (callable): The function to execute.
        max_retries (int): Maximum number of retries.
        delay (int): Delay in seconds between retries.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.

    Returns:
        The result of the function if successful.

    Raises:
        Exception: If all retries fail, the last exception is raised.
    """
    attempt = 0
    while attempt < max_retries:
        try:
            return func(*args, **kwargs)
        except (RuntimeError, ValueError, TypeError) as e:
            attempt += 1
            logger.warning("Attempt %d failed with error: %s", attempt, e)
            time.sleep(delay)

    logger.error("All retry attempts failed. for function {func.__name__}")
