# Student Attention Platform (SAP) - Student App

## Overview
The Student App is a core component of the Student Attention Platform (SAP), designed to monitor and report student engagement during online classes. The application uses webcam feeds to analyze student attention levels and provides real-time feedback to educators.

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
git clone https://github.com/SAP-Program/Student-App.git
```
2. Navigate to the student-app directory:
```bash
cd student-app
```
3. Install required dependencies:
```bash
pip install -r requirements.txt
```
4. Install submodules:
```bash
git submodule init
git submodule update
```

## Running the Application
```bash
python source/gui/login_page.py
```

## Directory Structure
student-app/
├── source/
├── └──
├──── gui/                 # GUI components
│     └── login_page.py    # Main application entry point
├──── backend/             # Attention analysis models
├── requirements.txt       # Python dependencies
├── README.md              # Documentation
├── .gitignore             # Git ignore file
└── .gitmodules            # Submodule data
