function DownloadFile($url, $targetFile) {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    $uri = New-Object "System.Uri" "$url"

    $request = [System.Net.HttpWebRequest]::Create($uri)

    $request.set_Timeout(15000) #15 second timeout

    $response = $request.GetResponse()

    $totalLength = [System.Math]::Floor($response.get_ContentLength() / 1024)

    $responseStream = $response.GetResponseStream()

    $targetStream = New-Object -TypeName System.IO.FileStream -ArgumentList $targetFile, Create

    $buffer = new-object byte[] 10KB

    $count = $responseStream.Read($buffer, 0, $buffer.length)

    $downloadedBytes = $count

    while ($count -gt 0) {

        $targetStream.Write($buffer, 0, $count)

        $count = $responseStream.Read($buffer, 0, $buffer.length)

        $downloadedBytes = $downloadedBytes + $count

        Write-Progress -activity "Downloading file '$($url.split('/') | Select -Last 1)'" -status "Downloaded ($([System.Math]::Floor($downloadedBytes/1024))K of $($totalLength)K): " -PercentComplete ((([System.Math]::Floor($downloadedBytes / 1024)) / $totalLength) * 100)

    }

    Write-Progress -activity "Finished downloading file '$($url.split('/') | Select -Last 1)'"

    $targetStream.Flush()

    $targetStream.Close()

    $targetStream.Dispose()

    $responseStream.Dispose()

}


$pythonUrl = "https://www.python.org/ftp/python/3.9.9/python-3.9.9-amd64.exe"
$targetDir = "$Env:USERPROFILE\AppData\Local\Programs\Python\Python399"
$tempDir = "$Env:USERPROFILE\AppData\Roaming\nightowl\temp"

Write-Output "Create directory $tempDir"
New-Item -ItemType directory -Path $tempDir -Force | Out-Null


$pythonNameLoc = $tempDir + "\python-3.9.9-amd64.exe"

$pythonExePathCaiTay = "$Env:USERPROFILE\AppData\Local\Programs\Python\Python39\python.exe"
$pythonExePath = $targetDir + "\python.exe"

if ((Test-Path -Path $pythonExePath -PathType Leaf) -or (Test-Path -Path $pythonExePathCaiTay -PathType Leaf)) {
    $pyversion = python --version
    Write-Output $pyversion
    if ($pyversion -ne "Python 3.9.9") {
        control appwiz.cpl

        Write-Host  "Vui long go cai dat tat ca cac phien ban Python khac 3.9.9 khoi may tinh cua ban, sau do chay lai tep nay." -ForegroundColor Red
        Write-Host  "Please uninstall all other Python versions 3.9.9 from your computer, then run this file again." -ForegroundColor Red
        exit 1
    }
}


$downloadFolder = (New-Object -ComObject Shell.Application).NameSpace('shell:Downloads').Self.Path
$pythonNameDownloadFolder = $downloadFolder + "\python-3.9.9-amd64.exe"

Write-Output "Check file $pythonExePath and $pythonExePathCaiTay"
$size = (Get-Item -Path $pythonNameLoc).Length







if (-not(Test-Path -Path $pythonExePath -PathType Leaf) -and -not(Test-Path -Path $pythonExePathCaiTay -PathType Leaf)) {



    Write-Output "Check file $pythonNameLoc"

    if ($size -ne 28829104) {

        if ((Test-Path -Path $pythonNameDownloadFolder -PathType Leaf)) {
            $pythonNameLoc = $pythonNameDownloadFolder
        }
        else {
            Write-Output "Create directory $targetDir"
            New-Item -ItemType directory -Path $targetDir -Force | Out-Null


            Write-Output "Download file $pythonUrl"
            downloadFile $pythonUrl $pythonNameLoc
        }
    }


    # These are the silent arguments for the install of python
    # See https://docs.python.org/3/using/windows.html
    $Arguments = @()
    $Arguments += "/i"
    $Arguments += 'InstallAllUsers="1"'
    $Arguments += 'TargetDir="' + $targetDir + '"'
    $Arguments += 'DefaultAllUsersTargetDir="' + $targetDir + '"'
    $Arguments += 'AssociateFiles="1"'
    $Arguments += 'PrependPath="1"'
    $Arguments += 'Include_doc="1"'
    $Arguments += 'Include_debug="1"'
    $Arguments += 'Include_dev="1"'
    $Arguments += 'Include_exe="1"'
    $Arguments += 'Include_launcher="1"'
    $Arguments += 'InstallLauncherAllUsers="1"'
    $Arguments += 'Include_lib="1"'
    $Arguments += 'Include_pip="1"'
    $Arguments += 'Include_symbols="1"'
    $Arguments += 'Include_tcltk="1"'
    # $Arguments += 'Include_test="0"'
    $Arguments += 'Include_tools="1"'
    $Arguments += "/passive"
    # $Arguments += "/quiet"

    Write-Output "Install Python"


    Start-Process $pythonNameLoc -ArgumentList $Arguments -Wait
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") +
    ";" +
    [System.Environment]::GetEnvironmentVariable("Path", "User")

}
else {
    Write-Output "Setup python ok"
}
# Get-Content requirements.txt | ForEach-Object { pip install $_ }
Get-Content requirements.txt | Where-Object { $_ -notmatch "^#" -and $_ -ne "" } | ForEach-Object { pip install $_ }
Write-Output "Done"
exit 0
# Start-Sleep -Seconds 1000
