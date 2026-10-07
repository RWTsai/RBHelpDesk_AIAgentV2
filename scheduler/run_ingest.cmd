@echo off
title RBIT 文件匯入
rem 文件匯入跑一輪。可以直接雙擊測試，也給排程工作呼叫。
rem conda 安裝路徑與環境名稱不同的話，改下面兩行就好。

cd /d "%~dp0.."

call "C:\ProgramData\anaconda3\Scripts\activate.bat"
call conda activate langgraph

python scheduler\ingest_docs.py --once >> "logs\ingest_task.log" 2>&1
