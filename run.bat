@echo off
echo Running Game...

:Ask
echo What test you want to launch?(1: Cards, 2: Floor, 3: GameTest)
set INPUT=
set /P INPUT=Type input: %=%
If /I "%INPUT%"=="1" goto CardsLaunch
If /I "%INPUT%"=="2" goto FloorLaunch
If /I "%INPUT%"=="3" goto GameLaunch

:CardsLaunch
python abyssaleclipse.py --cards
pause

:FloorLaunch
python abyssaleclipse.py --floor
pause

:GameLaunch
python abyssaleclipse.py --gametest
pause