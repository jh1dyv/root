@echo off

cd F:\Git\root\LwarpTest\start
del /s /q ..\test
copy /y *.py	..\test
copy /y *.tex	..\test
copy /y *.bat	..\test

set CWD=%CD%
cd ..\test

call :exec python escch_replace.py -v -d ../start/escch.replace enc *.tex
call :exec python csarg_replace.py -v enc *.tex
call :exec python insert_kludge.py

rem cd %CWD%
rem exit /b

call :exec pdflatex tutorial.tex

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
