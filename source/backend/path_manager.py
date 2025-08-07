from pathlib import Path
import os

if os.name == 'nt':
    BASE_DIR = Path("c:/sap-project")  # Set the base directory for Windows
else:
    BASE_DIR = Path.home() / "sap-project"  # Set the base directory for Linux/macOS

# Model and temporary image paths
INSIGHTFACE_DIR = BASE_DIR / ".insightface"  # Directory for insightface models