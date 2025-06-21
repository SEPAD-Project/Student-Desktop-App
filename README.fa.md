[![fa](https://img.shields.io/badge/lang-fa-blue.svg)](https://github.com/SEPAD-Project/Student-Desktop-App/blob/main/README.fa.md)
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/SEPAD-Project/Student-Desktop-App/blob/main/README.md)
# سپاد (مخفف عبارت فارسی سامانه پایش آنلاین دانش آموز) - Student Desktop App
این مخزن بخشی از پروژه SEPAD است و توسط [Abolfazl Rashidian](https://github.com/abolfazlrashidian) برای ورود دانش‌آموزان به کلاس و ارسال میزان توجه آنها به سرور توسعه داده شده است.

برای بازدید از سامانه سپاد، اینجا (https://github.com/SEPAD-Project) کلیک کنید.

## نمای کلی
این برنامه، ماژولی از SEPAD است که دانشجویان در طول کلاس‌های آنلاین آن را اجرا می‌کنند. این برنامه سه عملکرد اصلی را انجام می‌دهد: تجزیه و تحلیل تعامل چهره، نظارت بر پاسخ‌های اعلان‌ها و ردیابی فعالیت دسکتاپ - سپس نتایج را به سرور منتقل می‌کند.

## نیازمندی ها
قبل از نصب، مطمئن شوید که این الزامات را برآورده می‌کنید:
- Python 3.8 or higher
- Webcam supported by OpenCV
- Minimum hardware specifications:
  - Dual-core processor
  - 2GB RAM
  - 720p webcam

## نصب

1. مخزن را کلون کنید:
```bash
git clone https://github.com/SEPAD-Project/Student-Desktop-App.git
```
2. به دایرکتوری student-desktop-app بروید:
```bash
cd student-desktop-app
```
3.  یک محیط مجازی بسازید:
```bash
python -m venv .venv
```
4. محیط مجازی را فعال کنید:
```bash
.venv\Scripts\activate.bat
```
5. وابستگی های لازم را نصب کنید:
```bash
pip install -r requirements.txt
```
6.  ساب ماژول ها را نصب کنید:
```bash
git submodule init
git submodule update
```
>Head Position Estimation requires vs-build-tools for `InsightFace` to function properly. please read it readme file.

## اجرای اپلیکیشن
```bash
python RUN.py
```

## ساختار دایرکتوری
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

# 📬 تماس  
**Email**: SepadOrganizations@gmail.com  
**Issues**: [GitHub Issues](https://github.com/SEPAD-Project/Student-Desktop-App/issues)  