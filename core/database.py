import os
import csv
from core.config import DATA_DIR

def create_data_folder():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def initialize_file(
    file_path,
    headers
):
    if not os.path.exists(file_path):
        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:
            writer = csv.writer(file)
            writer.writerow(headers)

def read_file(file_path):
    try:
        with open(
            file_path,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        return []
    except Exception as error:
        print(
            "Error reading file:",
            error
        )
        return []

def write_file(
    file_path,
    headers,
    data
):
    try:
        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=headers
            )
            writer.writeheader()
            writer.writerows(data)
        return True
    except Exception as error:
        print(
            "Error writing file:",
            error
        )
        return False

def append_file(
    file_path,
    headers,
    data
):
    try:
        file_exists = (
            os.path.exists(file_path)
            and os.path.getsize(file_path) > 0
        )
        with open(
            file_path,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=headers
            )
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)
        return True
    except Exception as error:
        print(
            "Error appending file:",
            error
        )
        return False