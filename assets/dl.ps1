$url = '%url%'
$output = '%output%'
$sha256 = '%sha256%'

$wc = New-Object System.Net.WebClient
$wc.DownloadFile($url, $output)

# check if %sha256% is set
if ($sha256 -ne '') {
    $hasher = [System.Security.Cryptography.SHA256]::Create()
    $fileStream = [System.IO.File]::OpenRead($output)
    $hash = [System.BitConverter]::ToString($hasher.ComputeHash($fileStream)).Replace('-', '')
    Write-Host "Hash: $hash"
    $fileStream.Close()
    if ($hash -ne $sha256) {
        Write-Host 'Hash mismatch!!!'
        Remove-Item $output
        exit
    }
}