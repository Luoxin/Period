import sqlite3
import subprocess
import win32api
from time import sleep

import win32con
from gevent import os

print("正在进行环境准备..",end="")
try:
    conn = sqlite3.connect("Period.sqlite3")
    cursor = conn.cursor()
    sql = "create table Period (startDate text PRIMARY KEY,endDate text,takeDate Integer)"
    print("..",end="")
    cursor.execute(sql)
    cursor.close()
    conn.close()
except:
    pass

print("..",end="")
win32api.SetFileAttributes('Period.sqlite3', win32con.FILE_ATTRIBUTE_HIDDEN)  # 设置文件夹为隐藏

print("..",end="")
file=open("start.bat","w")
path=str(os.path.dirname(os.path.realpath(__file__)))
content='''@echo off
%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
cd /d "%~dp0"
set Program='''+path+'''\Period.exe
set LnkName=大姨妈
set WorkDir=
set Desc=大姨妈
if not defined WorkDir call:GetWorkDir "%Program%"
(echo Set WshShell=CreateObject("WScript.Shell"^)
echo strDesKtop=WshShell.SpecialFolders("DesKtop"^)
echo Set oShellLink=WshShell.CreateShortcut(strDesKtop^&"\%LnkName%.lnk"^)
echo oShellLink.TargetPath="%Program%"
echo oShellLink.WorkingDirectory="%WorkDir%"
echo oShellLink.WindowStyle=1
echo oShellLink.IconLocation="'''+path+'''\logo.ico" 
echo oShellLink.Description="%Desc%"
echo oShellLink.Save)>makelnk.vbs
makelnk.vbs
del /f /q makelnk.vbs
timeout /T 5
cmd /c "start .\Period.exe"
timeout /T 5
del /f /s /q .\Install.exe
del /f /q %0
exit
goto :eof
:GetWorkDir
set WorkDir=%~dp1
set WorkDir=%WorkDir:~,-1%
goto :eof'''
file.write(content)
file.close()

print("..",end="")
cmd=".\start.bat"
subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
sleep(2)
print("安装完成，正在为您启动程序")
cmd=".\del.bat"
subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
