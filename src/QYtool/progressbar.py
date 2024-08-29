"""
Name: progressbar.py
Author: Xuewen Zhang
Date:at 28/04/2024
version: 1.0.0
Description: my own toolbox for research projects
"""

from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
    TimeElapsedColumn,
    TaskProgressColumn,
    MofNCompleteColumn,
    SpinnerColumn,
    RenderableColumn,
)


class progressbar:

    def probar1():
        """ 
        Progress bar style 1:
            description: 5% =====----------------- 5/100 unit time elapsed < time remaining
        """
        progress = Progress(
            TextColumn(":hourglass_done: [progress.description]{task.description}"),
            TaskProgressColumn(),                              # percentage
            BarColumn(),
            MofNCompleteColumn(),                              # i/total
            TextColumn("[progress.unit]{task.fields[unit]}"),  # add unit
            TimeElapsedColumn(),                               # time elapsed
            TextColumn("<"),                                   # add a '<' symbol
            TimeRemainingColumn(),                             # time remaining
        )
        return progress


    def probar2():
        """ 
        Progress bar style 2:
            description: 5% =====----------------- 5/100 unit time elapsed < time remaining loss：0.00000
        """
        progress = Progress(
            TextColumn(":hourglass_done: [progress.description]{task.description}"),
            # SpinnerColumn(),
            TaskProgressColumn(),                              # percentage
            BarColumn(),                                       # progress bar
            MofNCompleteColumn(),                              # i/total
            TextColumn("[progress.unit]{task.fields[unit]}"),  # add unit
            TimeElapsedColumn(),                               # time elapsed
            TextColumn("<"),                                   # add a '<' symbol
            TimeRemainingColumn(),                             # time remaining
            TextColumn("loss:[progress.loss]{task.fields[loss]:.5f}"), # add wanted information
        )
        return progress
    
    def probar3(*args):
        """ 
        Progress bar style 3:
            description: 5% =====----------------- 5/100 unit time elapsed < time remaining args1：0.00000 args2: 0.00000 ....
        """
        text = []
        for arg in args:
            text.append(f"{arg}:[progress.{arg}]{{task.fields[{arg}]:.5f}}")
            
        progress = Progress(
            TextColumn(":hourglass_done: [progress.description]{task.description}"),
            # SpinnerColumn(),
            TaskProgressColumn(),                              # percentage
            BarColumn(),                                       # progress bar
            MofNCompleteColumn(),                              # i/total
            TextColumn("[progress.unit]{task.fields[unit]}"),  # add unit
            TimeElapsedColumn(),                               # time elapsed
            TextColumn("<"),                                   # add a '<' symbol
            TimeRemainingColumn(),                             # time remaining
            *(TextColumn(text_content) for text_content in text),  
        )
        return progress


if __name__ == "__main__":

    with progress:
        task1 = progress.add_task(description="[red]Downloading...", total=100, loss=0.0)
        i = 0
        while not progress.finished:
            i += 1
            loss = i * 0.001
            progress.update(task1, loss=loss, advance=1)
            time.sleep(0.02)