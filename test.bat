@echo off

set F=%1
if "%F%" equ "" (
	echo Usage: test file
	exit /b
)

set PATT=s/^^[\s]*[^^a-zA-Z0-9_\/#\\^&\{\}].*/\ ^&/

echo sed -e "%PATT%" 
nkf -s -Lw ..\%F% | sed -e "%PATT%" > %F%
exit /b
