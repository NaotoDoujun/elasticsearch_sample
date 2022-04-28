$WorkDir = "./"
$OutputDir = Join-Path $WorkDir "output"
If (-not (Test-Path $OutputDir)) { New-Item $OutputDir -ItemType Directory }

# 分割対象ファイル
$Inputfile = Join-Path $WorkDir "jawiki-latest-pages-articles.xml"

$PageCounter = 0
$Cycle = 1000 # 1ファイルに納める上限値
$Keyword = '</page>'
$FileBase = "File-"
$OutputFile = Join-Path $OutputDir $( $FileBase  + [string]$( $PageCounter / $Cycle ) + ".txt")
$TextData = New-Object System.Collections.ArrayList

Get-Date
Get-Content $InputFile -encoding utf8 | ForEach { 
 $TextData.Add($_) > $Null
 if ( $_ -match $Keyword ) {
  $PageCounter = $PageCounter + 1
  if ($PageCounter % $Cycle -eq 0) {
   $TextData -join "`n" | Out-File -FilePath $OutputFile -Encoding utf8
   $TextData = New-Object System.Collections.ArrayList
   $OutputFile = Join-Path $OutputDir $( $FileBase + [string]$( $PageCounter / $Cycle ) + ".txt")
   # 桁数を揃える場合 $( $PageCounter / $Cycle ).ToString("00000") に変更
  }
 }
}

$TextData -join "`n" | Out-File -FilePath $OutputFile -Encoding utf8

Get-Date
Write-Output "記事件数：${PageCounter}"


