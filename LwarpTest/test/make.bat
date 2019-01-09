@echo off

cd F:\Git\root\LwarpTest\start
del /s /q ..\test
copy /y *.py	..\test
copy /y *.tex	..\test
copy /y *.bat	..\test

set CWD=%CD%
cd ..\test

rem call :exec python escch_replace.py -v -d ../start/escch.replace enc *.tex
rem call :exec python csarg_replace.py -v enc *.tex
rem call :exec python insert_kludge.py

call :exec pdflatex tutorial.tex

cd %CWD%
exit /b

call :exec lwarpmk html
call :exec lwarpmk again
call :exec lwarpmk html
call :exec lwarpmk print
call :exec lwarpmk htmlindex
call :exec lwarpmk html
call :exec lwarpmk html1
call :exec lwarpmk limages
call :exec lwarpmk html

call :exec python csarg_replace.py -v dec *.html
call :exec python csarg_replace.py -v ren *.html
call :exec python escch_replace.py -v -d ../start/escch.replace dec *.html
call :exec python escch_replace.py -v -d ../start/escch.replace ren *.html

cd ..\start
exit /b

:exec
	echo ==== %* ====
	%*
	exit /b
