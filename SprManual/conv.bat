@echo off
set SRCF=%1
set SAVF=%1.org
rename %SRCF% %SAVF%
nkf -w %SAVF% > %SRCF%
exit /b
