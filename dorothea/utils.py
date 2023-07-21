import multiprocessing
import time

from Colors import *

def loading_animation(info):
    """
    Simple animation for running feedback

    Args:
        info(str): Message for animation

    Returns:
        None
    """
    animation = "|/-\\"
    i = 0
    while True:
        print(MAGENTA + info + " " + animation[i % len(animation)] + RESET, end='\r')
        #sys.stdout.flush()
        i += 1
        time.sleep(0.1)

def loading_decorator(task, title, info_msg):
    """
    Decorator for time consuming tasks

    Args:
        task: Task to wrap
        tile(str): Info strint to print at the end of task
        info_msg(str): Message for animation (passed to loading_animation())

    Returns:
        wrapper: Wraped function
    """
    def wrapper(*args, **kwargs):
        animation_process = multiprocessing.Process(target=loading_animation, args=(info_msg,))
        animation_process.start()
        result = task(*args, **kwargs)
        if isinstance(result, tuple):
            name = result[0].tags
        else:
            name = result.name
        print(GREEN + f"\t- {title} {name}" + RESET)
        animation_process.terminate()
        animation_process.join()
        return result
    return wrapper


def enlapsed_time_formater(elapsed_time_seconds):
    """
    Format a time stamp to H:M:S format

    Args:
        elapsed_time_seconds(float): Timestamp 

    Returns:
        (str): String with formated time
    """
    hours = int(elapsed_time_seconds // 3600)
    minutes = int((elapsed_time_seconds % 3600) // 60)
    seconds = int(elapsed_time_seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}" 


def time_to_refresh(info, t):
    """
    Dinamic countdown timer

    Args:
        info(str): Message for the timer
        t(float): Seconds for the timer
    
    Returns:
        None
    """
    for i in range(t, 0, -1):
        print(MAGENTA + f"{info}: {enlapsed_time_formater(i)}" + RESET, end='\r')
        time.sleep(1)