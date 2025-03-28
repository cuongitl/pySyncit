import json
import os
import shutil
import glob
import sys
import yaml
from datetime import datetime
import logging

# Set up logging
# current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
current_datetime = datetime.now().strftime("%Y%m%d")
log_file = f"iBackup_{current_datetime}.log"

logging.basicConfig(
	filename=log_file,
	level=logging.INFO,
	format='%(asctime)s - %(levelname)s - %(message)s'
)

# Log the start of the program
# logging.info("Program started.")

# Get the current working directory
current_dir = os.getcwd()
tmp_dir = f"{current_dir}/tmp"
file_config = os.path.join(current_dir, 'config.yml')

# file_config = 'config11.yml'

if not os.path.exists(file_config):
	logging.error(f"File {file_config} does not exist.")
	logging.error(f"file {file_config} does not exist")
	sys.exit()

if not os.path.exists(tmp_dir):
	os.makedirs(tmp_dir, exist_ok=True)


# Function to load the configuration from a YAML file
def load_config(file_path):
	with open(file_path, 'r') as file:
		return yaml.safe_load(file)


# SECTION-01: Function to handle copying of files or directories based on pattern
def copy_file_or_dir(_src, _dest, _update=False, _exclude=None):
	current_date = datetime.now().strftime("%Y%m%d")
	# Check if destination directory exists, create it if not
	try:
		if not os.path.exists(_dest):
			logging.info(f"Destination directory '{_dest}' does not exist. Creating it.")
			os.makedirs(_dest, exist_ok=True)
	except FileNotFoundError as e:
		logging.error(e)
		return
	# If src is a file, copy the file
	if os.path.isfile(_src):
		new_file_name = f"{os.path.splitext(os.path.basename(_src))[0]}_{current_date}.xlsx"
		dest_file = os.path.join(_dest, new_file_name)
		if not os.path.isfile(dest_file):
			if _exclude:
				file_ext = os.path.splitext(dest_file)[1]
				if file_ext in _exclude:
					return
			if _update and not is_modified(_src):
				return
			shutil.copy2(_src, dest_file)
			logging.info(f"Copied file: {_src} to {dest_file}")
	
	# If src is a directory (folder), copy the entire directory
	elif os.path.isdir(_src):
		# new_dest_dir = f"{dest}_{current_date}"
		new_dest_dir = f"{_dest}{current_date}"
		if not os.path.exists(new_dest_dir):
			os.makedirs(new_dest_dir)
		for file in os.listdir(_src):
			full_file_path = os.path.join(_src, file)
			if os.path.isfile(full_file_path):
				if _exclude:
					file_ext = os.path.splitext(full_file_path)[1]
					# print(f"file_ext: {file_ext}")
					if file_ext in _exclude:
						return
				if _update and not is_modified(full_file_path):
					continue
				shutil.copy2(full_file_path, new_dest_dir)
		logging.info(f"Copied directory: {_src} to {new_dest_dir}")
	
	# If src is a pattern (e.g., *.txt), copy matching files
	elif '*' in _src:
		matching_files = glob.glob(_src)
		for file in matching_files:
			new_file_name = f"{os.path.splitext(os.path.basename(file))[0]}_{current_date}.txt"
			dest_file = os.path.join(_dest, new_file_name)
			if _exclude:
				file_ext = os.path.splitext(file)[1]
				if file_ext in _exclude:
					return
			if _update and not is_modified(file):
				continue
			shutil.copy2(file, dest_file)
			logging.info(f"Copied {file} to {dest_file}")


# SECTION-02: File attributes are a type of metadata that describe and may modify how files and/or directories in a filesystem behave.
def get_file_attributes(_file_path):
	"""Get the attributes of the file."""
	return {
		'size': os.path.getsize(_file_path),
		'modified_time': os.path.getmtime(_file_path)
	}


def write_attributes_to_json(_file_path, _file_json):
	"""Write file attributes to a JSON file."""
	attributes = get_file_attributes(_file_path)
	with open(_file_json, 'w') as f:
		json.dump(attributes, f)


def read_attributes_from_json(_file_json):
	"""Read file attributes from a JSON file."""
	with open(_file_json, 'r') as f:
		return json.load(f)


def check_file_modified(_file_path, _file_json):
	"""Check if the file has been modified since the last check."""
	# print(f"{_file_json}")
	if not os.path.exists(_file_json):
		# If the JSON file does not exist, write the current attributes
		write_attributes_to_json(_file_path, _file_json)
		# print(f"Attributes written to JSON file: {_file_json}")
		return False  # File is considered not modified since it's the first run
	
	# Read the previous attributes from the JSON file
	previous_attributes = read_attributes_from_json(_file_json)
	current_attributes = get_file_attributes(_file_path)
	
	# Compare the current attributes with the previous attributes
	if current_attributes['size'] != previous_attributes['size'] or current_attributes['modified_time'] != previous_attributes['modified_time']:
		# File has been modified
		# print(f"{_file_path} - File has been modified.")
		logging.info(f"{_file_path} - File has been modified.")
		# Update the JSON file with the new attributes
		write_attributes_to_json(_file_path, _file_json)
		return True
	else:
		# print(f"{_file_path} - File has not been modified.")
		return False


def is_modified(_file_path):
	# Extract the filename
	file_name = os.path.basename(_file_path)
	# print(file_name)
	# without extension
	# file_name_without_ext = os.path.splitext(file_name)[0]
	# Define the JSON file name
	file_json = f"{tmp_dir}/{file_name}_attributes.json"
	# Check if the file has been modified
	return check_file_modified(_file_path, file_json)


