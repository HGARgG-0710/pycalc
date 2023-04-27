@echo off

@REM TODO: this is currently under consideration (no RUB available; ECB don't publish it, hence not available via this API currently;)...
@REM pip install forex-python

set Key=HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment
 
set FolderToAdd=%~dp0;
 
for /f "tokens=2*" %%a In ('Reg.exe query "%key%" /v Path^|Find "Path"') do set CurPath=%%~b
reg.exe add "%Key%" /v Path /t REG_EXPAND_SZ /d "%CurPath%;%FolderToAdd%" /f