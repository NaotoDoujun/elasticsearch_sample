$WorkDir = "./"
$OutputDir = Join-Path $WorkDir "output"

# Wikipedia XMLデータ
$Columns = "id", "timestamp", "title", "text"

$HeaderFile = Join-Path $WorkDir "xmlHeader.txt"
$FooterFile = Join-Path $WorkDir "xmlFooter.txt"

$HeaderText = Get-Content $HeaderFile -encoding UTF8
$FooterText = Get-Content $FooterFile -encoding UTF8

# Elasticsearch 登録先情報
$Hostname = "localhost"
$PortNumber = 9200
$IndexName = "wikipedia"
$BaseURL = "http://${Hostname}:${PortNumber}"

# map定義登録関数
Function Create-TypeItem ( [string]$JsonFilePath ) {
    $APIURL = "/${IndexName}"
    $TargetURL = $BaseURL + $APIURL
    $ReqestType = "PUT"
    $JsonData = Get-Content $JsonFilePath
    $PostParam = [System.Text.Encoding]::UTF8.GetBytes($JsonData)
    Invoke-RestMethod -Uri $TargetURL -Body $PostParam -ContentType 'application/json' -Method $ReqestType
    Write-Output $("`t Create-TypeItem( ${JsonFilePath} ) : " + $(Get-Date) )
}

# mapping定義
$JsonFilePath = Join-Path $WorkDir "map.json"
Create-TypeItem -JsonFilePath $JsonFilePath

# Bulkコマンド
$APIURL = "/${IndexName}/_bulk"
$RequestURL = $BaseURL + $APIURL
$ReqestType = "POST"
$BulkCommand = @{ "index" = @{ "_index" = $IndexName ; } } | ConvertTo-Json -Compress

# 投入対象一覧生成
$FileList = Get-ChildItem $OutputDir | Sort-Object -Property Name

ForEach ($File in $FileList) {

 # XML生成
 $PageText = Get-Content $File.Fullname
 [xml]$XMLData = $HeaderText + $PageText + $FooterText

 # Bulkコマンド用のJsonデータ生成
 $BulkData = New-Object System.Collections.ArrayList
 ForEach ($page in $XMLData.mediawiki.page) {
  $Row = New-Object PSObject | Select-Object $Columns
  $Row.id = $page.id
  $Row.timestamp = $page.revision.timestamp
  $Row.title = $page.title
  $Row.text = $page.revision.text."#text"
  $JsonData = $Row | ConvertTo-Json -Compress

  $BulkData.Add($BulkCommand) > $Null
  $BulkData.Add($JsonData) > $Null
 }

 # Bulk実行
 $JsonData = $( $BulkData -join "`n" ) + "`n"
 $PostParam = [System.Text.Encoding]::UTF8.GetBytes($JsonData)
 $Result = Invoke-RestMethod -Uri $RequestURL -Body $PostParam -ContentType 'application/json' -Method $ReqestType
 Write-Output $( $File.name + " : " + $(Get-Date) )
}

# 投入結果確認
$APIURL = "/${IndexName}/${TypeName}/_search"
$RequestURL = $BaseURL + $APIURL
$Result = Invoke-RestMethod -Uri $RequestURL
ConvertTo-JSON $Result -Depth 10