"""
# Author: https://t.me/Cuongitl
# Name:  pSyncit - Version: 1.0.0
# About: pSyncit is a simple tool designed to keep folders and files in sync with two modes: update and mirror.
- A mirror sync will adjust the destination folders/files to match the source folders/files by deleting any files and folders that exist in the destination location but do not appear in the source folders/files.
- An update sync will only copy new and updated files to the destination folders/files.
Synchronizing files between directories is a common task for managing backups, ensuring consistency across multiple storage locations, and keeping data organized.
While many tools are available for this purpose, creating a Python script for directory synchronization provides greater flexibility and control.
# Updated: 2025-03-28
"""
import logging

from run import *

if __name__ == '__main__':
    mode_update = False
    # Load the configuration from the YAML file
    config = load_config(file_config)
    # print(config)
    # Log the start of the program
    logging.info(f"Program started...running_mode: {config['mode']}")
    if config['mode'] == 'update':
        mode_update = True
    # print(f"mode_update: {mode_update}")
    for section in config:
        if section in ['mode']:
            continue
        print("*" * 25)
        path_info = config[section]
        print(f"section: {section} - path_info: {path_info}")
        src_dir = path_info[0]['src_dir']
        dest_dir = path_info[1]['dest_dir']
        exclude = None
        if len(path_info)> 2 and 'exclude' in path_info[2]:
            exclude = path_info[2]['exclude']
            # print(f"exclude: {path_info[2]['exclude']}")
        # print(f"src_dir: {src_dir}, \ndest_dir: {dest_dir}")
        if not src_dir or not dest_dir:
            logging.error(f"Error: 'src_dir' or 'dest_dir' missing in section '{section}'.")
            continue
        # Check if the source path exists
        if not os.path.exists(src_dir) and '*' not in src_dir:
            logging.error(f"Source path '{src_dir}' does not exist. Skipping.")
            continue
        # Handle the copying logic based on the src_dir pattern
        copy_file_or_dir(src_dir, dest_dir, _update=mode_update, _exclude=exclude)
    print("*" * 25)
    print("Done.")
