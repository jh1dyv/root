@echo off
del M.pdf
cmd /c nmake -f M.makefile tex
del main_2018*.pdf
cmd /c main.pdf
exit /b
