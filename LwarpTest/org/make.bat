@echo off

cd F:\Git\root\LwarpTest\start
copy /y ..\org\*.py .

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

exit /b

:exec
	echo ==== %* ====
	%*
	exit /b
