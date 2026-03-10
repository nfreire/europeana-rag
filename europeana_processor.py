import os
import zipfile
from typing import Callable

class EuropeanaDatasetProcessor:
    """
    A class to process Europeana dataset ZIP archives containing RDF/XML files.
    """

    def __init__(self, data_dir: str):
        """
        Initializes the processor with a data directory.

        Args:
            data_dir (str): Path to the folder containing ZIP archives.
        """
        self.data_dir = data_dir

    def process(self, handler: Callable[[str], None]):
        """
        Reads all ZIP files in the data directory and passes each RDF record's
        content to the handler.

        Args:
            handler (Callable[[str], None]): Function to handle the content of one RDF record.
        """
        if not os.path.exists(self.data_dir):
            raise FileNotFoundError(f"Data directory not found: {self.data_dir}")

        for filename in os.listdir(self.data_dir):
            if filename.endswith(".zip"):
                zip_path = os.path.join(self.data_dir, filename)
                self._process_zip(zip_path, handler)

    def _process_zip(self, zip_path: str, handler: Callable[[str], None]):
        """
        Processes a single ZIP archive.
        """
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                for member in zf.namelist():
                    # Check for RDF or XML files (avoid directories)
                    if (member.endswith(".rdf") or member.endswith(".xml")) and not member.endswith("/"):
                        with zf.open(member) as f:
                            content = f.read().decode('utf-8', errors='replace')
                            handler(content)
        except zipfile.BadZipFile:
            print(f"Warning: Skipping invalid ZIP file: {zip_path}")
        except Exception as e:
            print(f"Error processing {zip_path}: {e}")
