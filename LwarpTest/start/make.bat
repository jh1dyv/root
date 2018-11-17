@echo off

cd F:\Git\root\LwarpTest\start
del /s /q ..\test
copy /y *.py	..\test
copy /y *.tex	..\test
copy /y *.bat	..\test

cd ..\test

call :exec python csname_replace.py -v enc tutorial.tex
call :exec python insert_kludge.py

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

call :exec python csname_replace.py -v dec *.html
call :exec python csname_replace.py -v ren *.html

cd ..\start
exit /b

:exec
	echo ==== %* ====
	%*
	exit /b
