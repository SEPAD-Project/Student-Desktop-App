[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/SEPAD-Project/Student-Desktop-App/blob/main/README.md)
[![fa](https://img.shields.io/badge/lang-fa-blue.svg)](https://github.com/SEPAD-Project/Student-Desktop-App/blob/main/README.fa.md)
# SEPAD (The Persian acronym for Student Online Monitoring System) - Student Desktop App
This repository is a part of the SEPAD project and was developed by [Abolfazl Rashidian](https://github.com/abolfazlrashidian) for students to enter the class and send their attention level to the server.

Click [here](https://github.com/SEPAD-Project) to visit the SEPAD organization.

## Overview
This application is a module of SEPAD that students launch during online classes. It performs three core functions: analyzing facial engagement, monitoring notification responses, and tracking desktop activity - then transmits the results to the server.

## Requirements
Before installation, ensure you meet these requirements:
- Python 3.8 or higher
- Webcam supported by OpenCV
- Minimum hardware specifications:
  - Dual-core processor
  - 2GB RAM
  - 720p webcam

## Installation

1. Clone the repository:
```bash
git clone https://github.com/SEPAD-Project/Student-Desktop-App.git
```
2. Navigate to the student-desktop-app directory:
```bash
cd student-desktop-app
```
3. Create a virtual environment:
```bash
python -m venv .venv
```
4. Activate the virtual environment:
```bash
.venv\Scripts\activate.bat
```
5. Install required dependencies:
```bash
pip install -r requirements.txt
```
6. Install submodules:
```bash
git submodule init
git submodule update
```

## Running the Application
```bash
python run.py
```

## Directory Structure
```bash
student-desktop-app/
├── source/
├── └──
├──── gui/                 # GUI components
│     └── login_page.py    # Main application entry point
├──── backend/             # Attention analysis models
├── RUN.py                 # Run login page
├── requirements.txt       # Python dependencies
├── README.md              # Documentation
├── .gitignore             # Git ignore file
└── .gitmodules            # Submodule data
```

# 📝 Contribution  
1. Fork the repository  
2. Create feature branch (`git checkout -b feature/NewFeature`)  
3. Commit changes (`git commit -m 'Add NewFeature'`)  
4. Push to branch (`git push origin feature/NewFeature`)  
5. Open a Pull Request  

# 📬 Contact  
**Email**: SepadOrganizations@gmail.com  
**Issues**: [GitHub Issues](https://github.com/SEPAD-Project/Student-Desktop-App/issues)  