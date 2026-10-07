@echo off
title RBIT 文件匯入
rem 文件匯入跑一輪。可以直接雙擊測試，也給排程工作呼叫。
rem conda 安裝路徑與環境名稱不同的話，改下面兩行就好。

rem 放在 scheduler\ 或專案根目錄都可以：認 app.py 找專案根目錄
cd /d "%~dp0"
if not exist "app.py" cd ..
if not exist "app.py" (echo 找不到專案根目錄 & exit /b 1)

set PYTHONIOENCODING=utf-8

call "C:\ProgramData\anaconda3\Scripts\activate.bat"
call conda activate langgraph

python scheduler\ingest_docs.py --once >> "logs\ingest_task.log" 2>&1
