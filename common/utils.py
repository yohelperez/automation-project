import random
import time

def perform_action_with_delay(action, *args, **kwargs):
    """Perform the given action with a random delay."""
    action(*args, **kwargs)
    time.sleep(random.uniform(1, 3)) 