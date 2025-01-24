#!/usr/bin/env python3

"""

The purpose of this script is to add a specified folder and all its subfolders
to the Python path dynamically, allowing Python to locate and import modules 
from those directories in the current session.

Steps to Use This Script:

1. Save this script as `add_to_path.py`.
2. Make it executable:
   Run the command: `chmod +x add_to_path.py`
3. Execute it from the terminal with the folder path as an argument:
   Example: `./add_to_path.py /path/to/your/folder`
4. Optional: To run the script from anywhere:
   a. Move the script to a directory in your system's PATH:
      Example: `mv add_to_path.py /usr/local/bin/add_to_path`
   b. Now you can run it like this:
      `add_to_path /path/to/your/folder`
5. The script will add the specified folder and all its subfolders
   to the Python path for the current session.
"""
import sys
import os
import argparse

def add_folder_and_subfolders_to_path(folder_path):
    """
    Adds a folder and all its subfolders to the Python path.
    """
    for root, dirs, files in os.walk(folder_path):
        sys.path.append(root)
    print(f"Added {folder_path} and its subfolders to the Python path.")

def main():
    parser = argparse.ArgumentParser(description="Add a folder and its subfolders to the Python path.")
    parser.add_argument(
        "folder_path", 
        type=str, 
        help="The path to the folder you want to add to the Python path."
    )
    args = parser.parse_args()

    folder_path = os.path.abspath(args.folder_path)
    if os.path.exists(folder_path):
        add_folder_and_subfolders_to_path(folder_path)
    else:
        print(f"Error: The folder '{folder_path}' does not exist.")
        sys.exit(1)

if __name__ == "__main__":
    main()
