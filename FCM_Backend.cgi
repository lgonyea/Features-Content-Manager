#! /usr/bin/perl
##########################################

use strict;
#use warnings;
use Tie::File;
use File::Copy;
use CGI;
use utf8;
my $query = new CGI;
use encoding 'UTF-8';
require("FF_common_func.cgi");
require("FF_web_elements.cgi");
require("form_builder.cgi");
#my $baseFEfolder = "/Library/WebServer/CGI-Executables/FE2";
#my $FeatFolder = "/Library/WebServer/FF2";

my $timeStamp = GetTimeStamp();
my $thisFile;
my @specFiles;
my $fileToDo;
my ($homeIP,$systemType) = getHomeAddress();
my ($baseFEfolder,$FeatFolder) = getFilesLocal();
my @allbaseweeks = getweeks();
my $specDir = "$baseFEfolder/specs/";
my $histDir = "$baseFEfolder/BEHistory/";
my $trashDir = "${FeatFolder}/trash/";
my $tempDir = "$baseFEfolder/templates/";
my $userDir = "$baseFEfolder/users/";
my $xmlDir = "${FeatFolder}/xmlData/";
my $specTemplate = "/Library/WebServer/CGI-Executables/FormTemplates/specTemplate.spc";
my $xmlTempLocal = "$baseFEfolder/xmlTemplates/";
@specFiles = ArrayADir("$specDir","no");
my @specTempArray = arrayFile("$specTemplate");
#fileToDo should be only the feature name, no path or extension
my $fileToDo = $query->param('fileToDo');
# Mode is used to determine if we are going to edit, view, or save
my $pageMode = $query->param('Mode');
my $pageType = $query->param('pageType');
my $fileToGet = $query->param('DateToDo');
my $xmlFeat = $query->param('xmlFeat');

makeHTML5type();
LoadCSS();
print "<link href=\"/forms2.css\" rel=\"stylesheet\" media=\"screen\">\n";

LoadJS();
JQfadeIn("#Content","fast");

HTMLtitle("Gracenote FCM Backend Manager");

OpenDIV("ID","Header","");
makeHeaderTopper();
ClosedDIV("class","HeaderLeft","Gracenote FCM Backend Manager - $systemType");
EndDIV();

OpenDIV("ID","Nav");
#ClosedDIV("class","NavLeftNotUL","Pagetype - $pageType Mode is $pageMode");
#ClosedDIV("class","NavRight","<a href=\"http://$homeIP/cgi-bin/FE2/featuremanager.cgi\">FCM Editor</a>");
#ClosedDIV("class","NavRight","<a href=\"http://$homeIP/cgi-bin/FE2/featureDeadlines.cgi?deadlineweek=This Week\">Feature Deadline Manager</a>");
EndDIV();
#EndDIV();
OpenDIV("ID","Container");


OpenDIV("ID","Sidebar");

ClosedDIV("class","SidebarTitle","Edit A Spec File");
OpenDIV("class","SidebarGroup","","");
my $specDirDrop = getFileList("$specDir","");
ClosedDIV("class","SidebarChoice","<form method=\"get\" action=\"http://$homeIP/cgi-bin/FE2/FCM_Backend.cgi\"><select name=\"fileToDo\">\n$specDirDrop</select><input type=\"hidden\" name=\"pageType\" value=\"SpecEditor\"><input type=\"hidden\" name=\"Mode\" value=\"edit\"><input type=\"submit\" value=\"Edit Spec File\"></form>\n");
ClosedDIV("class","SidebarChoice","<form method=\"get\" action=\"http://$homeIP/cgi-bin/FE2/FCM_Backend.cgi\"><input type=\"hidden\" name=\"pageType\" value=\"SpecEditor\"><input type=\"submit\" value=\"Show All Spec Files\"></form>\n");
#ClosedDIV("class","SidebarChoice","<form method=\"get\" action=\"http://$homeIP/cgi-bin/FE2/FCM_Backend.cgi\"><input type=\"hidden\" name=\"pageType\" value=\"Recycle\"><input type=\"submit\" value=\"Show All Recovery Features\"></form>\n");
EndDIV();

ClosedDIV("class","SidebarTitle","Recycle a Feature");
OpenDIV("class","SidebarGroup","","");
my $xmlDatelist = "";
my @XMLtempFiles = ArrayADir("${FeatFolder}/xmlData","no");
	foreach (@XMLtempFiles) {
		my $getToDate = substr $_,8,8;
		my $xmlMonth = substr $getToDate,0,2;
		my $fixMonth = $xmlMonth;
		my $xmlDay = substr $getToDate,2,2;
		my $xmlYear = substr $getToDate,4,4;
		if ($xmlMonth =~ /^0/) {
			$fixMonth = substr $xmlMonth,1,1;
		} elsif ($xmlMonth =~ /^11/)  {
			$fixMonth = "n";
		} elsif ($xmlMonth =~ /^12/)  {
			$fixMonth = "d";
		} else {
			$fixMonth = "o";
					#$fixMonth = substr $xmlMonth,1,1;
		} 
		my $dateListing = "$fixMonth${xmlDay} ($xmlYear)";
		$xmlDatelist = ("$xmlDatelist<option value=\"$_\">$dateListing</option>\n");

	}

#my $xmlDatelist = convertMMDDYYYYtoMDD(@XMLtempFiles);
my $XMLtempFiles = getFileList("$xmlTempLocal","No");

ClosedDIV("class","SidebarChoice","<form method=\"get\" action=\"http://$homeIP/cgi-bin/FE2/FCM_Backend.cgi\"><select name=\"xmlFeat\">\n$XMLtempFiles</select>\n<select name=\"fileToDo\">\n$xmlDatelist</select>\n<input type=\"hidden\" name=\"status\" value=\"recycle\"><input type=\"hidden\" name=\"pageType\" value=\"recycle\"><input type=\"hidden\" name=\"Mode\" value=\"recycle\"><input type=\"submit\" value=\"View this feature\"></form>\n");
EndDIV();

ClosedDIV("class","SidebarTitle","Recycle a Feature");
OpenDIV("class","SidebarGroup","","");
ClosedDIV("class","SidebarChoice","<form method=\"get\" action=\"http://$homeIP/cgi-bin/FE2/FCM_Backend.cgi\"><input type=\"hidden\" name=\"pageType\" value=\"ArchiveSearch\"><input type=\"submit\" value=\"Search Feature Archives\"></form>\n");
EndDIV();

=begin New feature manager not ready for live
ClosedDIV("class","SidebarTitle","Create a new Feature");
OpenDIV("class","SidebarGroup","","");
#my $specDirDrop = getFileList("$specDir","No");
#ClosedDIV("class","SidebarChoice","<form method=\"get\" action=\"http://$homeIP/cgi-bin/FE2/FCM_Backend.cgi\"><select name=\"fileToDo\">\n$specDirDrop</select><input type=\"hidden\" name=\"pageType\" value=\"SpecEditor\"><input type=\"hidden\" name=\"Mode\" value=\"new\"><input type=\"submit\" value=\"Edit Spec File\"></form>\n");
ClosedDIV("class","SidebarChoice","<form method=\"get\" action=\"http://$homeIP/cgi-bin/FE2/FCM_Backend.cgi\"><input type=\"hidden\" name=\"pageType\" value=\"Feature Maker\"><input type=\"hidden\" name=\"Mode\" value=\"new\"><input type=\"submit\" value=\"Create a new Feature\"></form>\n");
EndDIV();
=cut New feature manager not ready for live

=begin New feature manager not ready for live

ClosedDIV("class","SidebarTitle","Edit a Template");
OpenDIV("class","SidebarGroup","","");
my $tempDirDrop = getFileList("$tempDir","");
ClosedDIV("class","SidebarChoice","<form method=\"get\" action=\"http://$homeIP/cgi-bin/FE2/FCM_Backend.cgi\"><select name=\"fileToDo\">\n$tempDirDrop</select><input type=\"hidden\" name=\"pageType\" value=\"TempEditor\"><input type=\"hidden\" name=\"Mode\" value=\"edit\"><input type=\"submit\" value=\"Edit Template File\"></form>\n");
#ClosedDIV("class","SidebarChoice","<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/FCM_Backend.cgi\"><input type=\"hidden\" name=\"pageType\" value=\"SpecEditor\"><input type=\"submit\" value=\"Show All Sepc Files\"></form>\n");
EndDIV();
=cut New feature manager not ready for live

=begin User manager not ready for live
ClosedDIV("class","SidebarTitle","User Manager");
OpenDIV("class","SidebarGroup","","");
my $userDirDrop = getFileList("$userDir","No");
ClosedDIV("class","SidebarChoice","<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/FCM_Backend.cgi\"><select name=\"fileToDo\">\n$userDirDrop</select><input type=\"hidden\" name=\"pageType\" value=\"UserEditor\"><input type=\"hidden\" name=\"Mode\" value=\"edit\"><input type=\"submit\" value=\"Manager User\"></form>\n");
#ClosedDIV("class","SidebarChoice","<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/FCM_Backend.cgi\"><input type=\"hidden\" name=\"pageType\" value=\"SpecEditor\"><input type=\"submit\" value=\"Show All Sepc Files\"></form>\n");
EndDIV();
=cut User manager not ready for live


#ClosedDIV("class","SidebarTitle","Recover Deleted Feature");
#OpenDIV("class","SidebarGroup","","");
#my $trashDirDrop = getFileList("$trashDir","Yes");
#ClosedDIV("class","SidebarChoice","<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/FCM_Backend.cgi\"><select name=\"fileToDo\">\n$trashDirDrop</select><input type=\"hidden\" name=\"pageType\" value=\"recover\"><input type=\"hidden\" name=\"Mode\" value=\"move\"><input type=\"submit\" value=\"Recover Feature\"></form>\n");
#ClosedDIV("class","SidebarChoice","<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/FCM_Backend.cgi\"><input type=\"hidden\" name=\"pageType\" value=\"SpecEditor\"><input type=\"submit\" value=\"Show All Sepc Files\"></form>\n");
#EndDIV();

EndDIV(); #End Sidebar


OpenDIV("ID","FormContent");

if ($pageType eq "recover") {
my @storyParts = split('\.',$fileToDo);
my $FeatWeek = $storyParts[1];
my $moveToFolder = "${FeatFolder}/${FeatWeek}/In Progress/$fileToDo";
my $moveFromFolder = "$trashDir$fileToDo";
my $tmp = "$tempDir$storyParts[0].tmp";
makeadir("$FeatWeek","In Progress");
#	ClosedDIV("class","ContentInfo","Moving feature from $moveFromFolder to $moveToFolder<br>");

move($moveFromFolder,$moveToFolder);
	my $completeAction = "$fileToDo has been recoverd and is available in the In Progress step for the week of $FeatWeek.";
	ClosedDIV("class","ContentInfo","Action Completed!<br>$completeAction<br>");
	ClosedDIV("class","ContentInfo","<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\"><input type=\"hidden\" name=\"tmp\" value=\"$tmp\"><input type=\"hidden\" name=\"fileLoc\" value=\"$moveToFolder\"><input type=\"hidden\" name=\"status\" value=\"In Progress\"><input type=\"hidden\" name=\"story\" value=\"$fileToDo\"><input type=\"hidden\" name=\"viewtype\" value=\"ViewOnly\"><input type=\"submit\" value=\"View $fileToDo\"></form>");

} elsif ($pageType eq "recycle") {
	#open this file $fileToGet
	#search for xmltemplate and $fileToDo.xml
	#search for regular template in $fileToDo.tmp
	#transfer to view mode with the ability to copy to a current available listings date.
		my $templateFile = "$baseFEfolder/templates/${xmlFeat}.tmp";
		my $openXML = "$xmlDir$fileToDo";
		#ClosedDIV("class","ContentInfo","Doing this xml $xmlDir$fileToDo<br> Looking for this feature $xmlFeat<br>");
				open FH, "<:encoding(UTF-8)", $openXML; #Get 
				my @records = <FH>;
				my $allrecords = join "", @records;	
				my $fieldCheck = $allrecords;
				close FH;
				$allrecords =~  /\<$xmlFeat\>(.*)\<\/$xmlFeat\>/s;
				my $thisFeat = $1;

		open TH,"<:encoding(UTF-8)",$templateFile or die $!;
		my @fieldlists = <TH>;
		close(TH);
		my $wholeFeat;
		foreach my $line (@fieldlists) {
			my @featfield = split('\|',$line);
 			my $fieldName = $featfield[0];
 			my $fieldType = $featfield[1];
 			my $fieldMarkup = $featfield[2];
 			my $fieldOption = $featfield[4];
 			chomp($fieldOption);
	#		ClosedDIV("class","ContentInfo","$thisFeat<br>");

 			$thisFeat =~ /\<$fieldName\>(.*)\<\/$fieldName\>/s; 
			my $fieldText = $1;
			
			if ($fieldCheck !~ /<$fieldName>/s) {
				my $fieldText = "";
			}

 	 	#	$fieldText = $query->escapeHTML($fieldText);
		if (($fieldName ne "EP") && ($fieldName ne "EOF") && ($fieldName ne "Notes") && ($fieldName ne "Photo")) {
 				$fieldText =~ s/\n/\<br\>/g;
 				$wholeFeat = "${wholeFeat}<br>$fieldText";
 					#ClosedDIV("class","ContentInfo","$fieldName<br><br>$fieldText");
			}
		}
	
	my $filenameList = "";
foreach my $thisDate (@allbaseweeks) {
		$filenameList = ("$filenameList<option value=\"${xmlFeat}.$thisDate\">${xmlFeat}.$thisDate</option>\n");
}
	print "<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\">";
	ClosedDIV("class","ContentInfo","Here is the feature text.<br>If you would like to copy this feature, please select the  week you wish to recycle this feature to<br><select name=\"story\">\n$filenameList</select><br><input type=\"submit\" name=\"actionDo\" value=\"Copy to this feature.\">\n");
	#ClosedDIV("class","ContentInfo","<input type=\"submit\" name=\"actionDo\" value=\"Copy to this feature.\"></form>\n");
	print "<input type=\"hidden\" name=\"tmp\" value=\"$templateFile\">";
	#print "<input type=\"hidden\" name=\"modtime\" value=\"$mod_time\">";
	print "<input type=\"hidden\" name=\"fileLoc\" value=\"$openXML\">";
	print "<input type=\"hidden\" name=\"status\" value=\"In Progress\">";
	#print "<input type=\"hidden\" name=\"story\" value=\"${xmlFeat}.$thisDate\">";
	print "<input type=\"hidden\" name=\"viewtype\" value=\"recycle\">";
	ClosedDIV("class","ContentInfoText","This is the feature file.<br>$wholeFeat<br>");


#my $fileToDo = $query->param('fileToDo');
# Mode is used to determine if we are going to edit, view, or save
#my $pageMode = $query->param('Mode');
#my $pageType = $query->param('pageType');
#my $fileToGet = $query->param('DateToDo');
#my $xmlFeat = $query->param('FeatName');

} elsif ($pageType eq "SpecEditor") {
	#ClosedDIV("class","formTitle","Spec File Editor for $fileToDo");

	if (($fileToDo eq "") && ($pageMode ne "new")) {
		#print "No spec file given. Showing list of spec files to edit.";
		foreach $thisFile (@specFiles) {
			#if (($thisFile =~ /^\./m) || ($thisFile eq "") || (!defined($thisFile))) {
			#	next;
			#} else {
				ClosedDIV("class","ContentCard","<form method=\"get\" action=\"http://$homeIP/cgi-bin/FE2/FCM_Backend.cgi\"><input type=\"hidden\" name=\"pageType\" value=\"SpecEditor\"><input type=\"hidden\" name=\"fileToDo\" value=\"$thisFile\"><input type=\"hidden\" name=\"Mode\" value=\"edit\"><input type=\"submit\" value=\"Edit $thisFile\"></form>");
			#}	
		} 
		
	#edit a given spec file
	
	} elsif ($pageMode eq "edit") {
		#Show the spec file to edit
		#print "Displaying spec file to edit - $specDir$fileToDo";
		print "<form id=\"specEdit\ method=\"post\" action=\"FCM_Backend.cgi\"><input type=\"hidden\" name=\"pageType\" value=\"SpecEditor\"><input type=\"hidden\" name=\"Mode\" value=\"update\"><input type=\"hidden\" name=\"fileToDo\" value=\"$fileToDo\">";
		#OpenDIV("class","formBox");
		#print "$specTemplate <br>$specDir$fileToDo <br>Editing $fileToDo<br>";
		MakeAForm("$specTemplate","$specDir$fileToDo","","Editing $fileToDo");
		print "<input type=\"submit\" value=\"Save $fileToDo\">";
		print "</form>";
		#EndDIV();
	} elsif ($pageMode eq "update") {
		#print "Updating $specDir$fileToDo<br>";
		#OpenDIV("class","formBox");
		ClosedDIV("class","formLine","$fileToDo has been updated! <form method=\"get\" action=\"http://$homeIP/cgi-bin/FE2/FCM_Backend.cgi\"><input type=\"hidden\" name=\"pageType\" value=\"SpecEditor\"><input type=\"submit\" value=\"Edit Another Spec File\"></form>\n");
		#ClosedDIV("class","formTitle","Updating $fileToDo");
		#PMaker("Copying to $histDir$fileToDo");
		move("$specDir$fileToDo","${histDir}${timeStamp}$fileToDo");
		my @specTempArray = arrayFile("$specTemplate");
		open SF,">","${specDir}${fileToDo}";
		foreach (@specTempArray) {
			my $writeLine = "";
			if ($_ =~ m/^#/) { #Line that starts with # symbol is informational about the columns
			} else {
				my @lineParts = split('\|',$_);
				my $fieldName = $lineParts[0];
				$fieldName =~ s/^\s+|\s+$//g;
				$writeLine = $query->param($fieldName);		
				OpenDIV("class","specVal");
				ClosedDIV("class","formLine","<label>$fieldName</label>");
				if ($writeLine eq '') {
					ClosedDIV("class","formInfo","No Value");
				} else {
					ClosedDIV("class","formInfo","$writeLine");
				}
				EndDIV();
				#ClosedDIV("class","formLine","$writeLine");
				#PMaker("$fieldName: $writeLine");
				print SF "$fieldName|$writeLine\n";
			}
		}
		#print "<p>$fileToDo has been updated!</p>";
		close SF;
		ClosedDIV("class","formLine","<form method=\"get\" action=\"http://$homeIP/cgi-bin/FE2/FCM_Backend.cgi\"><input type=\"hidden\"  name=\"fileToDo\" value=\"$fileToDo\"><input type=\"hidden\" name=\"pageType\" value=\"SpecEditor\"><input type=\"hidden\" name=\"Mode\" value=\"edit\"><input type=\"submit\" value=\"Edit $fileToDo again\"></form>\n");
#ClosedDIV("class","ContentInfoFoot","<form method=\"get\" action=\"http://$homeIP/cgi-bin/FE2/FCM_Backend.cgi\"><input type=\"hidden\" name=\"pageType\" value=\"SpecEditor\"><input type=\"submit\" value=\"Edit Another Spec File\"></form>\n");

		#EndDIV();
	} else {
	#	print "$fileToDo has been updated!";
	}
# End of SpecEditor
} elsif ($pageType eq "ArchiveSearch") {
	if ($pageMode eq "Search") { ## If user submitted a search parameter
	my $searchThis = $fileToDo; # what they're searching for
	my $featToSearch = $xmlFeat; # the features to look at
				my @featlist;
				## Get a list of all xml files from the xmldata directory
				my $xmlDataDir = opendir(DIR, $xmlDir);
					my @files = readdir DIR;
				    closedir(DIR);
					    foreach (@files) {
							if (($_ =~ /^\./m) || ($_ eq "") || (!defined($_))) {
							next;
							} 
							else {
							 @featlist = (@featlist,$_);
							}  
		 				 }
			#Make a list of templates. From the xml template directory.
				my @XMLtmpList;
				my $xmtmpDir = opendir(DIR, $xmlTempLocal);
					my @tmpfiles = readdir DIR;
				    closedir(DIR);
					    foreach (@tmpfiles) {
							if (($_ =~ /^\./m) || ($_ eq "") || (!defined($_))) {
							next;
							} 
							else {
							 @XMLtmpList = (@XMLtmpList,$_);
							}  
		 				 }
		 				 
		 if ($xmlFeat ne "All Features") { # User is searching in a particular feature
		 		my $templateFile = "$baseFEfolder/templates/${xmlFeat}.tmp";
		 		my $useTemplate = "$xmlDir/$xmlFeat.xmltmp";
		 		my $numberOfHits = 0;
		 	foreach (@featlist) { # repeats through all feature xml data files
		 		#ClosedDIV("Class","ContentInfo","$_<br>");
				my $featFound;
			 	open FH, "<", "$xmlDir/$_"; 
				my @XMLrecords = <FH>;
				my $allrecords = join "", @XMLrecords;	
				close FH;
				my $fieldCheck = $allrecords;	
					#ClosedDIV("Class","ContentInfo","Looking for $searchThis \n in $_<br><br>");
				if ($allrecords =~ /\<$xmlFeat\>/) {
					$allrecords =~ /\<$xmlFeat\>(.*)\<\/$xmlFeat\>/s; 	
					$featFound = $1;
					$featFound =~ s/\n/<br>/g;
					#ClosedDIV("Class","ContentInfo","Working on $featFound<br><br>");
					my $wholeFeat;
					if ($featFound =~ /$searchThis/) {
							#ClosedDIV("Class","ContentInfo","Using $templateFile<br>");
							my @fieldlists = getTmpNameList($templateFile);
							$featFound =~ s/$searchThis/\<mark\>$searchThis\<\/mark\>/g;
							my $thisFeatName;
							foreach my $fieldName (@fieldlists) {
 								my $fieldText;
 							if (($fieldName ne "EP") && ($fieldName ne "EOF") && ($fieldName ne "Notes") && ($fieldName ne "Photo")) {
 									$featFound =~ /\<$fieldName\>(.*)\<\/$fieldName\>/; 
									my $fieldText = $1;
									if ($fieldName eq "Name") {
 										$thisFeatName = $fieldText;
 									}
								#if ($featFound !~ /<$fieldName>/s) {
									#	my $fieldText = "";
									#} #if ($fieldCheck !~ /<$fieldName>/s)
 	 							#$fieldText = $query->escapeHTML($fieldText);
 								$fieldText =~ s/\n/<br>/g;
 								$wholeFeat = "${wholeFeat}<br>$fieldText";

									#ClosedDIV("class","ContentInfo","$fieldName<br><br>$fieldText");
								} #if (($fieldName ne "EOF")
							} #foreach my $line (@fieldlists) 
 							 $wholeFeat = "${wholeFeat}<br><hr><br>Recycle $thisFeatName<br>";
							 $wholeFeat = "${wholeFeat}<br><form method=\"get\" action=\"http://$homeIP/cgi-bin/FE2/FCM_Backend.cgi\"><input type=\"hidden\" name=\"pageType\" value=\"recycle\"><input type=\"hidden\" name=\"Mode\" value=\"recycle\">";
							$wholeFeat = "${wholeFeat}<input type=\"hidden\" name=\"status\" value=\"recycle\"><input type=\"hidden\" name=\"xmlFeat\" value=\"$xmlFeat\"><input type=\"hidden\" name=\"fileToDo\" value=\"$_\"><input type=\"submit\" value=\"Recycle $thisFeatName\"></form>\n";
						ClosedDIV("Class","ContentInfo","$wholeFeat");

					} #if ($featFound =~ /$searchThis/)
					#	ClosedDIV("Class","ContentInfo","$wholeFeat<br>");

########
				} #if ($allrecords =~ /\<$xmlFeat\>/)
			 	#ClosedDIV("Class","ContentInfo","$wholeFeat<br>");
			########
			} #foreach (@featlist)
		 } #if ($searchThis ne "All Features")
		 else 
		 { 
		 	ClosedDIV("Class","ContentInfo","Searching all features for $searchThis");

				foreach my $xmlFile (@featlist) {
			 			open FH, "<", "$xmlDir/$xmlFile"; 
						my @XMLrecords = <FH>;
						my $allrecords = join "", @XMLrecords;
						close FH;
						my $thisXML = $allrecords;
		
					if ($allrecords =~ /$searchThis/) { #If the XML file contains the search, loop through all templates and identify which one(s) they are.
								ClosedDIV("Class","ContentInfo","$xmlFile contains $searchThis");
								foreach my $xmltemplate (@XMLtmpList) {
								my $useTemplate = "$xmlDir$xmltemplate";
								my $featFound;
								my @Parts = split('\.',$xmltemplate);
								my $featName = $Parts[0];
								my $templateFile = "$baseFEfolder/templates/${featName}.tmp";
						if ($allrecords =~ /\<$featName\>/) {
							$allrecords =~ /\<$featName\>(.*)\<\/$featName\>/s; 	
							$featFound = $1;
							$featFound =~ s/\n/<br>/g;
							#ClosedDIV("Class","ContentInfo","Working on $featFound<br><br>");
							my $wholeFeat;
							if ($featFound =~ /$searchThis/) {
									#ClosedDIV("Class","ContentInfo","Using $templateFile<br>");
									$featFound =~ s/$searchThis/\<mark\>$searchThis\<\/mark\>/g;
									#ClosedDIV("Class","ContentInfo","Yay, $featName contains $searchThis<br>$featFound");
									my @fieldlists = getTmpNameList($templateFile);
									my $thisFeatName;
									foreach my $fieldName (@fieldlists) {
		 								my $fieldText;
		 							if (($fieldName ne "EP") && ($fieldName ne "EOF") && ($fieldName ne "Notes") && ($fieldName ne "Photo")) {
		 									$featFound =~ /\<$fieldName\>(.*)\<\/$fieldName\>/; 
											my $fieldText = $1;
											if ($fieldName eq "Name") {
		 										$thisFeatName = $fieldText;
		 									}
										#if ($featFound !~ /<$fieldName>/s) {
											#	my $fieldText = "";
											#} #if ($fieldCheck !~ /<$fieldName>/s)
		 	 							#$fieldText = $query->escapeHTML($fieldText);
		 								$fieldText =~ s/\n/<br>/g;
		 								$wholeFeat = "${wholeFeat}<br>$fieldText";

											#ClosedDIV("class","ContentInfo","$fieldName<br><br>$fieldText");
										} #if (($fieldName ne "EOF")
									} #foreach my $line (@fieldlists) 
		 							 $wholeFeat = "${wholeFeat}<br><hr><br>Recycle $thisFeatName<br>";
									 $wholeFeat = "${wholeFeat}<br><form method=\"get\" action=\"http://$homeIP/cgi-bin/FE2/FCM_Backend.cgi\"><input type=\"hidden\" name=\"pageType\" value=\"recycle\"><input type=\"hidden\" name=\"Mode\" value=\"recycle\">";
									$wholeFeat = "${wholeFeat}<input type=\"hidden\" name=\"status\" value=\"recycle\"><input type=\"hidden\" name=\"xmlFeat\" value=\"$featName\"><input type=\"hidden\" name=\"fileToDo\" value=\"$xmlFile\"><input type=\"submit\" value=\"Recycle $thisFeatName\"></form>\n";
								ClosedDIV("Class","ContentInfo","$wholeFeat");

							} #if ($featFound =~ /$searchThis/)
							#	ClosedDIV("Class","ContentInfo","$wholeFeat<br>");

						} #if ($allrecords =~ /\<$xmlFeat\>/)

						}
					}
				}
			}
	} else { ## If no search was submitted, give the user the form to fill out.
	
				 my $XMLtempFiles = getFileList("$xmlTempLocal","No");
				 $XMLtempFiles = ("<option value=\"All Features\">All Features</option>$XMLtempFiles\n");


				print "<form method=\"get\" action=\"FCM_Backend.cgi\"><input type=\"hidden\" name=\"pageType\" value=\"ArchiveSearch\"><input type=\"hidden\" name=\"Mode\" value=\"Search\">";
				ClosedDIV("Class","ContentInfo","Welcome to Feature Archive search<br>Please enter text to search for:<br><input type=\"text\" maxlength=\"50\" cols=\"10\" name=\"fileToDo\" value=\"$fileToDo\"><br><br>Now select from the dropdown what feature to search. You can also choose to search all features back to October 2014.<br><select name=\"xmlFeat\">\n$XMLtempFiles</select><br><br><input type=\"submit\" name=\"search\" value=\"Search\"></form>");
				#ClosedDIV("class","formLine","<input type=\"text\" maxlength=\"50\" cols=\"10\" name=\"fileToDo\" value=\"$fileToDo\">");
				#ClosedDIV("class","ContentInfo","Now select from the dropdown what feature to search. You can also choose to search all features back to October 2014.<br><select name=\"xmlFeat\">\n$XMLtempFiles</select><br><input type=\"submit\" name=\"search\" value=\"Search\"></form>");
				#ClosedDIV("class","formLine","<select name=\"xmlFeat\">\n$XMLtempFiles</select><input type=\"submit\" name=\"search\" value=\"Search\">");
				#ClosedDIV("class","formLine","<input type=\"text\" maxlength=\"50\" cols=\"10\" name=\"fileToDo\" value=\"$fileToDo\" AUTOFOCUS>");
				#ClosedDIV("class","formSub","<input type=\"submit\" name=\"search\" value=\"Search\">");
	}	 

} elsif ($pageType eq "Feature Maker") {

	if ($pageMode eq "new") {
				OpenDIV("class","formBox");
				ClosedDIV("Class","formTitle","Welcome to Feature Maker interface");
				print "<form method=\"post\" action=\"FCM_Backend.cgi\"><input type=\"hidden\" name=\"pageType\" value=\"Feature Maker\"><input type=\"hidden\" name=\"Mode\" value=\"Validate\">";
				ClosedDIV("class","formLine","Please choose a name for this new feature. <br>The name cannot be longer than 8 characters and cannot match another feature name.");
				ClosedDIV("class","formLine","Once we have a good name, we will create a spec file on the next page.");
				ClosedDIV("class","formLine","<input type=\"text\" maxlength=\"8\" cols=\"10\" name=\"fileToDo\" value=\"$fileToDo\" AUTOFOCUS>");
				ClosedDIV("class","formSub","<input type=\"submit\" name=\"next\" value=\"NEXT\>\">");
				EndDIV();
	}
		if ($pageMode eq "Validate") {
				my $featFound = "FALSE";
				
				foreach (@specFiles) {
					if ("$_" eq "${fileToDo}.spc") {
						$featFound = "TRUE";
					}
				}
				if ($featFound eq "FALSE") {
					OpenDIV("class","formBox");
					ClosedDIV("Class","formTitle","Welcome to Feature Maker interface");
					print "<form method=\"post\" action=\"FCM_Backend.cgi\"><input type=\"hidden\" name=\"pageType\" value=\"Feature Maker\"><input type=\"hidden\" name=\"Mode\" value=\"maker\">";
					ClosedDIV("class","formLine","Great, we will now edit the spec file for $fileToDo.<br> Please choose the values for this feature. ");
					ClosedDIV("class","formLine","We will create the feature template on the next page.");
					ClosedDIV("class","formLine","");
					
					MakeAForm("$specTemplate","new","","Spec file for $fileToDo","$fileToDo");
					ClosedDIV("class","formSub","<input type=\"submit\" name=\"next\" value=\"NEXT\>\">");
					EndDIV();
				} else {
					OpenDIV("class","formBox");
					ClosedDIV("Class","formTitle","Welcome to Feature Maker interface");
					print "<form method=\"post\" action=\"FCM_Backend.cgi\"><input type=\"hidden\" name=\"pageType\" value=\"Feature Maker\"><input type=\"hidden\" name=\"Mode\" value=\"Validate\">";
					ClosedDIV("class","formLine","OOPS! The name you chose $fileToDo already exists. Please choose another name.");
					ClosedDIV("class","formLine","Please choose a name for the new feature. The name cannot be longer than 8 characters and cannot match another feature name.");
					ClosedDIV("class","formLine","Once we have a good name, we will create a spec file on the next page.");
					ClosedDIV("class","formLine","<input type=\"text\" maxlength=\"8\" name=\"fileToDo\" value=\"$fileToDo\" AUTOFOCUS>");
					ClosedDIV("class","formSub","<input type=\"submit\" name=\"next\" value=\"NEXT\>\">");
					EndDIV();	
				}
	}

} else {
ClosedDIV("class","ContentBoxPlain","Welcome to the Features Content Management Backend Sytem.</p><p>Please choose form the menus to manage aspects of this interface</p>");
}
EndDIV(); #Content

EndDIV(); #Container
HTMLend();