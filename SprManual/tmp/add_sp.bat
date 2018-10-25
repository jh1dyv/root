@echo off
setlocal enabledelayedexpansion

set CWD=%CD%
if "%CWD:~-3%" neq "tmp" (
echo Run at "tmp"	
exit /b
)

set FILES= intro.tex getstarted.tex structure.tex base.tex foundation.tex collision.tex physics.tex graphics.tex fileio.tex humaninterface.tex creature.tex framework.tex embpython.tex unity.tex trouble.tex
set FILES=intro.tex

set PATT=s/^^[ \t]*[^^a-zA-Z0-9_ \.=\t\/#$^%\\^&\(\)\{\}].*/\\KLUDGE ^&/

set PATT=s/\([\u3400-\u9fff\uf900-\ufaff\\ud840-\ufaff\udc00-\udfff]\)/\\KLUDGE \1/

for %%f in (%FILES%) do (
	echo add_sp: %%f ^(-^> %%f.org^)
	if not exist %%f.org (
		rename %%f %%f.org
	)
	rem echo "%PATT%"
	nkf -s %%f.org | sed -e "%PATT%" | nkf -w > %%f
)

endlocal
exit /b
