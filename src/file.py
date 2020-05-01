import csv
import os.path
from typing import *


class File:
    T = TypeVar("T")

    @staticmethod
    def process(filename: str, processing: Callable[[str, str], T]) -> List[T]:
        """Process a CSV file"""

        # Check if the file exists
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File {filename} does not exist")

        # Get the CSV header
        with open(filename, encoding="utf-8-sig") as f:
            # Get the first element of the CSV file
            header: List[str] = next(csv.reader(f))

        # Check if the Time column is present
        if "Time" not in header:
            raise RuntimeError(f"'Time' column not found in file {filename}")

        # Remove the Time column, since it doesn't hold actual data
        header.remove("Time")

        # Create a list of results
        results = []

        # Process each column in the header
        for column in header:
            results.append(processing(filename, column))

        return results
