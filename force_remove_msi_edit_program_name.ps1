Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*' | Where-Object DisplayName -like 'Cloudflare WARP*' | ForEach-Object {

    $_
    Remove-Item $_.PSPath

}

Get-ItemProperty -Path 'HKLM:\SOFTWARE\Classes\Installer\Products\*' | Where-Object ProductName -like 'Cloudflare WARP*' | ForEach-Object {

    $_
    Remove-Item -Recurse $_.PSPath

}
