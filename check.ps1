param($file,$source)


$XMLfile=$file
[XML]$packageReferences=Get-Content $XMLfile
$results=@()
foreach($packageReference in $packageReferences.Project.ItemGroup.PackageReference) {
	$results += $packageReference.Include +' ' + $packageReference.Version
}

$outputs=@()
$outputs = nuget list -Source $source

$outcomes=@()
foreach($result in $results) {
     if ($outputs.Contains($result) -eq $false -And $outcomes.Contains($result) -eq $false ) {
	$index = $result.Lastindexof('0') +1
	if($index -eq $result.Length){
	    $result1=$result+'.0'
	    $result2=$result.Substring(0, $result.Length-2)
	    if($outputs.Contains($result1) -eq $false -And $outputs.Contains($result2) -eq $false) {
        	 $outcomes += $result  
		}
	  }
	else {
		$outcomes += $result  
	}
     }
 }
$outcomes

foreach ($outcome in $outcomes) {
	$space=$outcome.Indexof(" ")
     	$key=$outcome.Substring(0,$space)
     	$value = $outcome.Substring($space+1)
        nuget install $key -Version $value -OutputDirectory $source
} 
























