import re
from pydicom.tag import Tag
from pydicom.dataset import Dataset


def flatten_dicom_dataset(dataset: Dataset) -> dict:
    flattened = {}

    # Define a recursive function to handle nested sequences
    def _flatten_element(ds, prefix=""):
        for elem in ds:
            # Skip pixel data which is typically very large
            if elem.tag == Tag("PixelData"):
                continue

            # Create a readable tag name
            if elem.keyword:
                key = f"{prefix}{elem.keyword}"
            else:
                key = f"{prefix}{elem.tag}"

            # Handle sequences (nested datasets)
            if elem.VR == "SQ":
                # For each item in the sequence
                for i, item in enumerate(elem.value):
                    _flatten_element(item, prefix=f"{key}[{i}].")
            else:
                # Regular element, just add it
                flattened[key] = elem.value

    _flatten_element(dataset)
    return flattened


def extract_index(string):
    # Pattern to match digits inside square brackets
    pattern = r"\[(\d+)\]"

    # Search for the pattern in the string
    match = re.search(pattern, string)

    # If found, return the digit as an integer
    if match:
        return int(match.group(1))

    # Return None or raise an exception if no match is found
    return None
