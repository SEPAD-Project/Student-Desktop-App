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
```bash
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
```

# 📝 Contribution  
1. Fork the repository  
2. Create feature branch (`git checkout -b feature/NewFeature`)  
3. Commit changes (`git commit -m 'Add NewFeature'`)  
4. Push to branch (`git push origin feature/NewFeature`)  
5. Open a Pull Request  

# 📬 Contact  
**Email**: sapOrganizations@gmail.com  
**Issues**: [GitHub Issues](https://github.com/SAP-Program/Student-App/issues)  

# 📜 License (MIT)  
```text
MIT License

Copyright (c) 2023 SAP Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```