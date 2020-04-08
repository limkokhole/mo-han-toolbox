@echo off
setlocal
set cookies=%locallib_usretc%\cookies.bilibili.txt
set workdir=%locallib_usrdl%

if not defined root set root=%workdir%
pushd %root%
call :%*
popd
goto :eof

:i
call :id2url %*
you-get -c %cookies% -i %url%
goto :eof

:l
set /p "url=#URL: "
if not defined url goto :l
if "%url%"=="q" goto :eof
start /min cmd /c call bilidl d %url%
goto :l

:d
if exist "%~1" (
for /f "delims=" %%i in ("%~1") do call :urlhandler %%i
) else call :urlhandler %*
goto :eof

:download
you-get -c %cookies% %*
goto :eof

:rename
for %%i in ("%~1.*") do (
echo "%%~i" -^> "%~2%%~xi"
move /y "%%~i" "%~2%%~xi" >nul
)
goto :eof

:urlhandler
call :id2url %*
call :bilidl_worker %url%
goto :eof

:bilidl_worker
bilidl_worker.py %* && timeout /t 3 && goto :eof
timeout /t 10
goto :bilidl_worker
goto :eof

:id2url
set id=%*
if %id:~,1%==[ set id=%id:~1%
if %id:~-1%==] set id=%id:~,-1%
if %id:~,4%==http set url=%id%
if %id:~,2%==BV set url=https://b23.tv/%id%
if %id:~,2%==av set url=https://b23.tv/%id%
if %id:~,2%==AV set url=https://b23.tv/av%id:~2%
echo %url%
goto :eof
