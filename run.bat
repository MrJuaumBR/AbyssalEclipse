@echo off

:menu
cls
echo Which code do you want to run?
echo 1. Cards Test
echo 2. Game Test
echo 3. Floor Test
echo X. Exit

set /p choice=Enter your choice: 

if %choice%==1 goto code1
if %choice%==2 goto code2
if %choice%==3 goto code3
if %choice%==X goto exit

echo Invalid option. Please try again.
pause
goto menu

:code1
echo Running Cards Test...
python ./abyssaleclipse.py --cards
goto menu

:code2
echo Running Game Test...
python ./abyssaleclipse.py --gametest
goto menu

:code3
echo Running Floor Test...
python ./abyssaleclipse.py --floor
goto menu

:exit
echo Exiting...
exit