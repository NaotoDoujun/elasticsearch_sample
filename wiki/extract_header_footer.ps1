$WorkDir = "./"
$OutputDir = Join-Path $WorkDir "output"

$FileList = Get-ChildItem $OutputDir | Sort-Object -Property "LastWriteTime"
$FirstFile = $FileList | Select-Object -First 1
$LastFile = $FileList | Select-Object -Last 1

$FirstFile.FullName
$LastFile.FullName

Copy-Item $FirstFile.FullName $WorkDir
Copy-Item $LastFile.FullName $WorkDir

$LineCounter = 0
$Keyword = '<page>'
$Header = New-Object System.Collections.ArrayList
[System.Collections.ArrayList]$FirstFileData = Get-Content $FirstFile.FullName

ForEach ($Line in $FirstFileData) {
 if ( $Line.Contains($Keyword) ) {break}
 $Header.Add($Line) >$Null
 $LineCounter = $LineCounter +1
}
$LineCounter
$Header

$HeaderFile = Join-Path $WorkDir "xmlHeader.txt"
$Header  -join "`n" | Out-File -FilePath $HeaderFile -Encoding utf8

$FirstFileData[0]
$FirstFileData[$LineCounter]

ForEach ($i in @(1..$LineCounter) ) {
 $FirstFileData.RemoveAt(0)
}

$FirstFileData[0]
$FirstFileData -join "`n" | Out-File -FilePath $FirstFile.FullName -Encoding utf8

[System.Collections.ArrayList]$LastFileData = Get-Content $LastFile.FullName
$LastLine = @($LastFileData).length -1
$LastFileData[$LastLine]

$FooterFile = Join-Path $WorkDir "xmlFooter.txt"
$LastFileData[$LastLine] | Out-File $FooterFile -Encoding UTF8

$LastFileData.RemoveAt($LastLine)
@($LastFileData).length

$LastFileData -join "`n" | Out-File -FilePath $LastFile.FullName -Encoding utf8

