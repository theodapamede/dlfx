from importlib.metadata import version, PackageNotFoundError

from .dicom import flatten_dicom_dataset, extract_index
from .utils import stamp_notebook

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "unknown"
