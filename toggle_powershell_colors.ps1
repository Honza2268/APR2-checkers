try {
    Get-ItemPropertyValue -Path "HKCU:\Console" -Name "VirtualTerminalLevel"
    Remove-ItemProperty -Path "HKCU:\Console" -Name "VirtualTerminalLevel"
    Write-Output "Succesfuly added registry key"
}
catch {
    New-ItemProperty -Path "HKCU:\Console" -Name "VirtualTerminalLevel" -Value "0x1" -PropertyType "DWORD"
    Write-Output "Succesfuly removed registry key"
}