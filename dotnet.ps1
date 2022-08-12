param($root, $projectlocation)



$SOLUTIONROOT = $root
[System.Collections.ArrayList]$packageslist = @();

Function ListAllPackages ($BaseDirectory)
{
    $PACKAGECONFIGS = Get-ChildItem -Recurse -Force $BaseDirectory -ErrorAction SilentlyContinue | 
        Where-Object { ($_.PSIsContainer -eq $false) -and  ( $_.Name -eq "packages.config")}
        
    ForEach($PACKAGECONFIG in $PACKAGECONFIGS)
        {
            $path = $PACKAGECONFIG.FullName
            
            $xml = [xml]$packages = Get-Content $path
            		    
                            foreach($package in $packages.packages.package)
                            {
                                if($package.developmentDependency -ne "true") {
                                     $entry ="`n`t`t<PackageReference Include=`"$($package.id)`" Version=`"$($package.version)`" Framework=`"$($package.targetFramework)`" />"
   				     $packageslist.Add($entry) 
					
                                 } 
			   }
	  
               
        }
   
}

Function CreateProjectFile ($projectlocation)
{
    $uniqueList = $packageslist | Sort-Object  | Get-Unique

    $start = '<Project Sdk="Microsoft.NET.Sdk.Web">

      <PropertyGroup>
        <TargetFramework>net48</TargetFramework>
      </PropertyGroup>

      <ItemGroup>'

      $end = "</ItemGroup>

    </Project>"

$total = $start + $uniqueList + $end
$total | Out-File $projectlocation
    
}

ListAllPackages $SOLUTIONROOT
CreateProjectFile $projectlocation


