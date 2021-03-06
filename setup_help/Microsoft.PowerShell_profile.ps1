# Created: 190507
# Objective: a windows-version ".bashrc" file that can help preload helpful commands.

Set-Alias -Name python -Value python.exe
function aserver {ssh -i C:\Users\kris\.ssh\id_rsa -p 1122 root@141.69.58.230}
function bserver {ssh -i C:\Users\kris\.ssh\id_rsa -p 2422 root@141.69.58.230}
function heimdall {ssh -i C:\Users\kris\.ssh\id_rsa iki@141.69.58.223}

function ipython {ipython.exe --nosep}

Set-Alias -Name sumatra -Value "C:\Program Files\SumatraPDF\SumatraPDF.exe"
Set-Alias -Name npp -Value "C:\Program Files (x86)\Notepad++\notepad++.exe"
Set-Alias -Name foxit -Value "D:\Programs2\FoxitReader\FoxitReader.exe"

function cpprun{
    echo "SYSTEM: building..."
    g++ -std=c++11 $args
    if($?){
        echo "SYSTEM: Success, running..."
        echo ""
        .\a.exe
    }
}
