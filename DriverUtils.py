import time
import random

class DriverUtils:

    @staticmethod
    def clear_input(*args):
        try:
            for x in args:
                x.clear()
        except Exception:
            # driver.quit()
            print("Not a clearable web element!")

    @staticmethod
    def print_current_action(action_string):
        print(action_string + "...     ", end='')

    @staticmethod
    def print_action_result(ok=True):
        if not ok:
            print("[failure]")
        else:
            print("[success]")

    @staticmethod
    def wait_random_time(start=0.5, end=3.0):
        random.seed()
        time.sleep(random.uniform(start, end))
