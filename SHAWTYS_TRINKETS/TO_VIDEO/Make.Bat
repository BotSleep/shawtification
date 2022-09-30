cd %appdata%/../../anaconda3/scripts/
call activate
cd %~dp0
call python makeVideo.py
pause