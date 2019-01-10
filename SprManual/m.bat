@echo off
setlocal enabledelayedexpansion
set path=F:\C-Drive-Save\texlive\2014\bin\win32;%path%

cmd /c make clean
cmd /c make
cmd /c main.pdf

endlocal
exit /b
