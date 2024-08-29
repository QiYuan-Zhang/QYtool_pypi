"""
Name: dirtool.py
Author: Xuewen Zhang
Date:at 03/05/2024
version: 1.0.0
Description: my own toolbox for research projects
"""


import os
import re
import shutil
from rich import print as rprint


class dirtool(object):
    def __init__(self):
        self.author = 'Xuewen Zhang'
        
    
    def create_new_folder_with_max_number(self, directory, prefix=''):
        """
            In the given directory, create a new folder that have a larger number than folders already exist.
            For example: In the directory, have folders mx1, mx2, then create folder mx3
            directory: given path
            prefix: the beginning part of the filenames that you want to check for, e.g. 'exp1', 'exp2' then prefix='exp'
        """
        # check if exit the path, if not, create it.
        self.makedir(directory)

        # Get a list of all folders in the directory
        folders = [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]

        # Filter out folders that match the specified pattern
        pattern = re.compile(rf"{prefix}(\d+)")
        matching_folders = [folder for folder in folders if pattern.match(folder)]

        # Extract numbers from matching folder names
        numbers = [int(pattern.match(folder).group(1)) for folder in matching_folders]

        # Find the maximum number
        max_number = max(numbers) if numbers else 0

        # Create a new folder with the maximum number incremented by 1
        new_folder_name = f"{prefix}{max_number + 1}"
        new_folder_path = os.path.join(directory, new_folder_name)
        os.makedirs(new_folder_path)

        return new_folder_name, new_folder_path
    

    def makedir(self, *args):
        """Create the directory"""
        for item in args:
            if not os.path.exists(item):
                os.makedirs(item)
        return
                
                
    def removedir(self, *args):
        """Delete the directory"""
        for item in args:
            shutil.rmtree(item)
        return 
                

    def current_dir(self):
        """Get the path of current file"""
        current_directory = os.path.dirname(os.path.realpath(__file__))
        return current_directory
    

    def copy_file(self, destination_directory, *args):
        """
            Copy the source_file to the destination directory, and generate an info.txt give the original copied file path
            destination_directory (str): destination directory
            args (str): source_file
        """
        for source_file in args:
            try:
                self.makedir(destination_directory)

                # Copy the file to the destination directory
                copied_file_name = os.path.basename(source_file)
                destination_file = os.path.join(destination_directory, copied_file_name)
                shutil.copy(source_file, destination_file)

                # Generate a text file with the content of the original file path and copied file name
                original_file_name = os.path.splitext(copied_file_name)[0]  # Extract filename without extension
                txt_file_path = os.path.join(destination_directory, f"{original_file_name}_info.txt")
                with open(txt_file_path, "w") as txt_file:
                    txt_file.write(f"Original file path: {source_file}\n")
                    txt_file.write(f"Copied file name: {copied_file_name}")

                rprint(f"[cyan] :clipboard: File [white]'{source_file}'[/white] copied to [white]'{destination_directory}'[/white] as [white]'{copied_file_name}'[/white] with [white]'{original_file_name}_info.txt'[/white] [green]successfully[/green].")
            except FileNotFoundError:
                raise ValueError(f"Source file {source_file} not found.")
            except PermissionError:
                raise ValueError("Permission denied.")
            except Exception as e:
                raise ValueError(f"An error occurred: {e}")