cd %appdata%/../../anaconda3/scripts
call activate
cd %~dp0 
python MOVE_BINOUT.py
pause