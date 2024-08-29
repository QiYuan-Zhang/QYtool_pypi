"""
Name: timer.py
Author: Xuewen Zhang
Date:at 28/04/2024
version: 1.0.0
Description: my own toolbox for research projects
"""
import time
from rich import print as rprint

def timer(f):
    def wrapper(*args, **kwargs):
        start = time.time()
        ret = f(*args, **kwargs)
        end = time.time()
        rprint(f":stopwatch:  Function: [cyan]{f.__name__}[/cyan] ==> Time elapsed: [orange]{end-start:.3f}[/orange] s")
        return ret
    return wrapper