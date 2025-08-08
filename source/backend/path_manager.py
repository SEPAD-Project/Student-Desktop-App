from pathlib import Path
import os

# Set base directory based on OS
if os.name == 'nt':
    BASE_DIR = Path("c:/sap-project")  # Windows
else:
    BASE_DIR = Path.home() / "sap-project"  # Linux/macOS

# Ensure base directory exists
BASE_DIR.mkdir(parents=True, exist_ok=True)

# Model and image paths
INSIGHTFACE_DIR = BASE_DIR / ".insightface"
REAL_STUDENT_IMAGE = BASE_DIR / "real_image.jpg"  
REGISTERED_STUDENT_IMAGE = BASE_DIR / "registered_image.jpg"

# Model paths - using Path for cross-platform compatibility
BUFFALO_MODEL_PATH = INSIGHTFACE_DIR / "models" / "buffalo_l.zip"
BUFFALO_MODEL_EXTRACT_PATH = INSIGHTFACE_DIR / "models" / "buffalo_l"

# Ensure insightface directory exists
INSIGHTFACE_DIR.mkdir(parents=True, exist_ok=True)