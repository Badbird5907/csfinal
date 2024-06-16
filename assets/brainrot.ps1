$workingDir = '%cwd%'
$titleb64 = 'VGhpcyBnYW1lIGJvcmluZyBhaCBoZWxsIPCfkoA='
$titleDecoded = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($titleb64))

$exepath = $workingDir + '/assets/ffplay.exe'
$videopath = '%vid%'

$cmd = $exepath + ' -alwaysontop -loop 0 -an %moreargs% -window_title ''' + $titleDecoded + ''' -vf ''scale=360:640'' -i ' + $videopath
Write-Host $cmd
Invoke-Expression $cmd