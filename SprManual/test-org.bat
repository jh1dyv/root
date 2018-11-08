@echo off
setlocal enabledelayedexpansion

set CWD=%CD%
if "%CWD:~-9%" equ "SprManual" (set DO_PDF=yes&set DO_LWARP=yes)
if "%CWD:~-3%" equ "tmp" (set DO_LWARP=yes)

if "%DO_PDF%" equ "yes" (
	python buildhtml.py -v -K -t %* main_html.tex
)
if "%DO_LWARP%" equ "yes" (
	call :exec lwarpmk html
	call :exec lwarpmk again
	call :exec lwarpmk html
	call :exec lwarpmk print
	call :exec lwarpmk htmlindex
	call :exec lwarpmk html
	call :exec lwarpmk html1
	call :exec lwarpmk limages
	call :exec lwarpmk html
)

endlocal
exit /b

:exec
	echo ====[ %* ]====
	%*
	exit /b
