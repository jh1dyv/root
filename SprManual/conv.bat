@echo off

if "%1" equ "" goto :end
echo %1
type %1 | sed -e "s/{sourcecode}/{sourcecode}/g" | sed -e "s/\([^\']\)zw/\1\\zw/g" | sed -e "s/^%%iflwarp(\(.*\))/\1/g" | nkf -w > tmp\%1
shift
:end
exit /b
