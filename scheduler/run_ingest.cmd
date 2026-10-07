@echo off
title RBIT 文件匯入
rem 雙擊＝畫面上看得到過程；排程器帶 /q 參數＝輸出寫進 logs\ingest_task.log
rem conda 安裝路徑或環境名稱不同的話，改下面兩行就好。

rem 放在 scheduler\ 或專案根目錄都可以：認 app.py 找專案根目錄
cd /d "%~dp0"
if not exist "app.py" cd ..
if not exist "app.py" echo 找不到專案根目錄 & goto end
if not exist "logs" md logs

set PYTHONIOENCODING=utf-8
call "C:\ProgramData\anaconda3\Scripts\activate.bat"
call conda activate langgraph

if "%~1"=="/q" goto quiet

echo 目錄：%CD%
python -c "import sys;print('Python:', sys.executable)"
echo.
python scheduler\ingest_docs.py --once
echo.
echo ---- 結束碼 %ERRORLEVEL%（0 代表成功）----

:end
pause
exit /b

:quiet
python scheduler\ingest_docs.py --once >>"logs\ingest_task.log" 2>&1
