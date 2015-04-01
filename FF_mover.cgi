#! /usr/bin/perl
## Larry Gonyea TMS 8/6/2013
### FF_mover basically moves files around to the various directories based on the cgi parameters.
### See what actions happen in the comments below to see where certain actions happen.
 
#use warnings;
use strict;
use Tie::File;
use File::Copy;
use CGI;
use File::Find;
use URI::Escape;
#use utf8;
#use encoding 'UTF-8';
require("FF_common_func.cgi");
require("FF_web_elements.cgi");
#my $baseFEfolder = "/Library/WebServer/CGI-Executables/FE2";
#my $FeatFolder = "/Library/WebServer/FF2";
my ($baseFEfolder,$FeatFolder) = getFilesLocal();
my $query = new CGI;
my ($homeIP,$systemType) = getHomeAddress();
#file example: "/Library/WebServer//Sites/Default/FF2/$datefolder/$statParam/$nameParam";
my $thistmp = $query->param('tmp');
my $featfile = $query->param('fileLoc');
my $newstatParam = $query->param('newstate');
my $oldstate = $query->param('oldstate');
my $storyName = $query->param('story');
my $actionDo = $query->param('actionDo');
my $prevFilter = $query->param('backlink');
my $CanCopy;
my @copyNameSP;
my $copyTmp;
my $copyFile;
my $refiltered = "FALSE";
my $RecycleThis = "FALSE";
my $completeAction;
my @errorList = "";
my $problemsFound = "False";
my $homeDir = "$FeatFolder/";
my $liveList = "$baseFEfolder/liveFeatList.txt";
my $date;
my $featPreview;
my @fileparts = split('/',$featfile);
my $filename = $fileparts[6];
my $tempOrDate = $fileparts[4];
my $process_time = 10;
my @storyparts = split('\.',$filename);
my $featName = $storyparts[0];
my $specFile = "$baseFEfolder/specs/$featName.spc";

if (($oldstate eq "filtered") && ($newstatParam eq "filtered")) {
	my $refiltered = "TRUE";
	my $refilterText = $query->param('refiltext');
}
#Check to see if we want to recycle this feature for later
#my %checkforTest = hashAFile($specFile);
#my $checkTest = $checkforTest{'status'};
#my $checkTest = checkLiveFeat("$featName");
#my $checkTest = checkFileforText($featName,$liveList);

if ($tempOrDate eq "Temp") {
	$date = $storyparts[1];
} else {
	$date = $fileparts[4];
}

if ($oldstate eq "trash") {
 my $newstatParam = "trash";
}
my %GetFeatSpecs = hashAFile($specFile);
my $checkCopy = $GetFeatSpecs{'copy'};
my $checkRecycle = $GetFeatSpecs{'recycle'};
my $checkTest = $GetFeatSpecs{'status'};

if ($checkTest eq "live") {
	$checkTest = "LIVE";
} else {
	$checkTest = "TEST";
}

if ($checkRecycle eq "Yes") {
 $checkRecycle = "TRUE";
} else {
 $checkRecycle = "FALSE"; 
}

if ($checkCopy ne "copy") {
my $CanCopy = "TRUE";
} else {
my $CanCopy = "FALSE"; 
}
if ($newstatParam eq "copy") {
	@copyNameSP = split('\.',$storyName);
	$copyTmp = "$baseFEfolder/templates/$copyNameSP[0].tmp";
	$copyFile = "$FeatFolder/$date/In Progress/$storyName";
}

## establish base directories.
my $histDir = "$FeatFolder/History/$date/$newstatParam/$filename"; #where file will go for back up.
my $RecycleDir = "$FeatFolder/Recycle/$filename"; #where file will go for back up.
my $newfeat = "$FeatFolder/$date/$newstatParam/$filename"; #where new feature will go when saved.
my $filterfeat = "$FeatFolder/$date/Posted/$filename"; #where filtered version will go while having an html version still in the Posted folder.
#my @featSpecs = getFeatSpecs($featName);

makeHTML5type();
LoadCSS();
LoadJS();
JQfadeIn("#Content","slow");
HTMLtitle("Gracenote Feature Writer");
OpenDIV("ID","Header");
makeHeaderTopper();

ClosedDIV("class","HeaderLeft","<b>$filename</b></br>");
EndDIV();
OpenDIV("ID","Container");

OpenDIV("ID","Content");

## if reset was passed, in both old and new states, this is a new feature that hasn't been written to yet.

if (($newstatParam eq "reset") && ($oldstate eq "reset")) { 

	my $moveFromFile = $featfile;
	my @dirParts = split('/',$featfile);
	my $stepPart = $dirParts[5];
	my @storyparts = split('\.',$storyName);
	my $dateFolder = $storyparts[1];
	my $moveToFile = "$FeatFolder/$dateFolder/$stepPart/$storyName";
	move($moveFromFile,$moveToFile);
	$completeAction = "$filename has been reset and can be Edited again.";
	ClosedDIV("class","ContentInfo","Action Completed!<br>$completeAction");
	ClosedDIV("class","ContentEditFull","<a href=\"http://$homeIP/cgi-bin/FE2/featuremanager.cgi\"><button>Return Main Page</button></a>");
	
	## if reset was passed, the feature needs to move from the TEMP folder to it's original state. This is used when a feature was being edited but a user left the feature in the
##       middle of the edit. This function is called by the main featureman site. 
} elsif ($newstatParam eq "copy") {
	makeadir($date,"In Progress");
	my $record;
	my $Tagged;
	my $lineToCopy;
	my %oldFeatHash;
	my $CGIlist;
	#print "Opening $featfile<br> Using template $thistmp";
	open FH, "<:encoding(UTF-8)", $featfile; #Get existing feature and put all together to grab text between name tags
	my @records = <FH>;
	my $allrecords = join "", @records;	
	close FH;
	my @cgiListNames = getTmpNameList($thistmp);
		foreach $CGIlist (@cgiListNames) {
		  #chomp($CGIlist);
		  #print "This is the template name <$CGIlist>\n";
			if (($CGIlist eq "EP") || ($CGIlist eq "Hidden") || ($CGIlist eq "EOF")) { 
			#Do nothing. Don't want these.
			} else {
				$allrecords =~ /\<$CGIlist\>(.*)\<\/$CGIlist\>/; 
				$record = $1;
				chomp($record);
				#print "$CGIlist record is: $record<br>";
				$oldFeatHash{$CGIlist} = $record;
			}
		}
	#print "Opening to write to $copyFile<br> TMP file is $copyTmp<br>";
	open CF, ">:encoding(UTF-8)", $copyFile; #Get existing feature and put all together to grab text between name tags
	my @copyTags = getTmpNameList($copyTmp);
		foreach $Tagged (@copyTags) {
			#print "Looking to get the $Tagged section<br>";
			$lineToCopy = $oldFeatHash{$Tagged};
			#print "to CF $Tagged - $lineToCopy\n";
			if ($Tagged eq "Name") {
			print CF "<Name>$storyName</Name>\n";
			} else {
## ADD CPSTYLE here
			if ($storyName =~ /^tor/) {
				#$lineToCopy = convertToCPStyle($lineToCopy);
				$lineToCopy = runFilter("cpstyle",$lineToCopy);
			}
			print CF "<$Tagged>$lineToCopy</$Tagged>\n";
			}
		}
	close CF;
	#copy($featfile,$copyFile)
	$completeAction = "Successfully copied from $filename. Feature $storyName is now availble to edit.";
				if ($storyName =~ /^tor/) {
					$completeAction = "Feature converted to CP style\<br>$completeAction";
				}
ClosedDIV("class","ContentInfo","Action Completed!<br>$completeAction");
	$featPreview = MakeAPreview($copyTmp,$copyFile,$storyName);
	ClosedDIV("class","ContentEditFull",$featPreview);
	ClosedDIV("class","ContentInfoFoot","End of $storyName");
#	ClosedDIV("class","ContentEditFull","<a href=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi/\"><button>Edit $storyName Now</button></a>");
EndDIV();	
	OpenDIV("ID","Sidebar");
		ClosedDIV("class","SidebarTitle","Return to Main page");
		OpenDIV("class","SidebarGroup");
			ClosedDIV("class","SidebarChoice","<a href=\"http://$homeIP/cgi-bin/FE2/featuremanager.cgi\"><button>Main Page</button></a>");
		EndDIV();
		ClosedDIV("class","SidebarTitle","Edit $storyName now");
			OpenDIV("class","SidebarGroup");
			ClosedDIV("class","SidebarChoice","<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\"><input type=\"hidden\" name=\"tmp\" value=\"$copyTmp\"><input type=\"hidden\" name=\"fileLoc\" value=\"$copyFile\"><input type=\"hidden\" name=\"status\" value=\"In Progress\"><input type=\"hidden\" name=\"story\" value=\"$storyName\"><input type=\"submit\" value=\"Edit $storyName\"></form>");
			#<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\"><input type=\"hidden\" name=\"tmp\" value=\"$thistmp\"><input type=\"hidden\" name=\"fileLoc\" value=\"$featfile\"><input type=\"hidden\" name=\"status\" value=\"$newstatParam\"><input type=\"hidden\" name=\"story\" value=\"$storyname\"><input type=\"submit\" value=\"Open $lFile\"></form>"
		EndDIV();
		if ($newstatParam ne "copy") {
		ClosedDIV("class","SidebarTitle","Continue Editing this Feature");
			OpenDIV("class","SidebarGroup");
			ClosedDIV("class","SidebarChoice","<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\"><input type=\"hidden\" name=\"tmp\" value=\"$thistmp\"><input type=\"hidden\" name=\"fileLoc\" value=\"$featfile\"><input type=\"hidden\" name=\"status\" value=\"$newstatParam\"><input type=\"hidden\" name=\"story\" value=\"$filename\"><input type=\"submit\" value=\"Return to editing $filename\"></form>");
			#<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\"><input type=\"hidden\" name=\"tmp\" value=\"$thistmp\"><input type=\"hidden\" name=\"fileLoc\" value=\"$featfile\"><input type=\"hidden\" name=\"status\" value=\"$newstatParam\"><input type=\"hidden\" name=\"story\" value=\"$storyname\"><input type=\"submit\" value=\"Open $lFile\"></form>"
		EndDIV();
	}
} elsif ($newstatParam eq "reset") {
	my $moveFromFile = $featfile;
	my @dirParts = split('/',$featfile);
	my $stepPart = $dirParts[5];
	my @storyparts = split('\.',$storyName);
	my $dateFolder = $storyparts[1];
	if ($oldstate ne "new") {
	my $moveToFile = "$FeatFolder/$dateFolder/$stepPart/$storyName";
	move($moveFromFile,$moveToFile);
	}
	$completeAction = "Successfully quit $filename without making changes.";
	ClosedDIV("class","ContentInfo","Action Completed!<br>$completeAction");
	ClosedDIV("class","ContentEditFull","<a href=\"http://$homeIP/cgi-bin/FE2/featuremanager.cgi\"><button>Return Main Page</button></a>");

## Trashing a feature happens from the feature_editor script. 	
## This moves the feature to a Trash folder created in the dated folder. 
## Currently, this feature can only be recovered by manually moving it from the Trash folder to the date/step folder.

} elsif ($newstatParam eq "trash") { 
	my @dirParts = split('/',$featfile);
	my $stepPart = $dirParts[5];
	my @storyparts = split('\.',$storyName);
	my $dateFolder = $storyparts[1];
	makeadir("Trash");
 	my $moveFromFile = $featfile;
	my $moveToFile = "${homeDir}/Trash/$storyName";
 	move($moveFromFile,$moveToFile);
	$completeAction = "$filename has been deleted and will now show in the list of new features available.";
	#emailnotifier($oldstate,"trash",$featfile,$featName,$specFile);
	ClosedDIV("class","ContentInfo","Action Completed!<br>$completeAction");
	#<a href=\"http://$homeIP/cgi-bin/FE2/featuremanager.cgi/\"><button>Return Main Page</button></a>");
	ClosedDIV("class","ContentEditFull","<a href=\"http://$homeIP/cgi-bin/FE2/featuremanager.cgi/\"><button>Return Main Page</button></a>");


## If this feature is not being reset or trashed, it must be moving. 
## We'll take all the fields and write the new feature to the correct date/step folder.
## This makes a tagged file that we can open up again with the Feature Editor. Tags are based on the fieldname in the TMP file. 

} elsif ($oldstate eq "preview") { 
	#my $featPreview = "";
	$featPreview = MakeAPreview($thistmp,$featfile,$featName);
	ClosedDIV("class","ContentEditFull",$featPreview);
	ClosedDIV("class","ContentInfoFoot","End of $filename");


} else { 
	#my $featPreview = "";
	my @cgiListNames = getTmpNameList($thistmp);
	makeadir($date,$newstatParam);
	makeahistdir($date,$newstatParam);
	open FEAT,">:encoding(UTF-8)",$newfeat;

	foreach my $CGIlist (@cgiListNames) {
		chomp($CGIlist);
		my $markEnd = "";
		my @lineValues = getTMPLinevalues($thistmp,$CGIlist);
		
		# [0] = field name
		# [1] = text field type
		# [2] = merlmarkup 
		# [3] = default text
		# [4] = optional field marker indicated by "Opt"

		my $markStart = getMerltoHtmlMark($thistmp,$CGIlist);
		#my $markStart = $lineValues[2];
		if (($CGIlist eq "EP") || ($CGIlist eq "Hidden") || ($CGIlist eq "EOF")) { 
			#$featPreview = "$featPreview<br>";#Don't add these until we are ready for production.
		} elsif ($CGIlist eq "Notes") {
			my $this_line = $query->param($CGIlist);
			$this_line =~ s/\n+/\<br>/g; #change new lines to html breaks 
			print FEAT "<${CGIlist}>${this_line}</${CGIlist}>\n";
		} elsif ($CGIlist eq "Photo") {
			my $this_line = $query->param($CGIlist);
			$this_line =~ s/\n+/\<br>/g; #change new lines to html breaks 
			print FEAT "<${CGIlist}>${this_line}</${CGIlist}>\n";
		} else {
			my $this_line = $query->param($CGIlist);
			#$this_line =~ uri_escape_utf8($this_line);
			utf8::decode($this_line);
			#print "Line is $this_line\n";
			$this_line =~ s/\s+/ /g; #find more than one space together replace with single space
			$this_line =~ s/\n+/\<br>/g; #change new lines to html breaks 
			$this_line =~ s/\<br \/>/\<\/p> \<p>/g; #change new lines to html breaks
			if (($featName ne "soapsyn") && ($featName ne "selspsyn") && ($featName ne "whatdvr")) {
			$this_line =~ s/<\/strong><\/p> <p>/<\/p> <p><\/strong>/g;
			}
			#$this_line =~ s/&nbsp;/ /g; #find more than one space together replace with single space
			#utf8::decode($this_line);
			#$this_line =~ s/\x{201d}/\"/g;
			#$this_line =~ s/\x{201c}/\"/g;			
			#$this_line =~ s/\x{2019}/\'/g;
			#$this_line =~ s/\x{2018}/\'/g;
			#$this_line =~ s/\x{2018}/\'/g;	
			#utf8::encode($this_line);
			#$this_line =~ s/\"/ \&quot /g; #change double quotes to html double quote
			print FEAT "<${CGIlist}>${this_line}</${CGIlist}>\n";
		}
	}

	close FEAT;
	chmod(0755,$newfeat);
	$featPreview = MakeAPreview($thistmp,$newfeat,$featName);

	#put the  file in the history directory for feature forensics. 
	if ($oldstate ne 'new') {
		move($featfile,$histDir); 
	}
	$completeAction = "$filename has been updated from <b>$oldstate</b> to step <b>$newstatParam</b>.";
	if ($newstatParam ne "Filtered") {
		ClosedDIV("class","ContentInfo","Action Completed!<br>$completeAction");
		ClosedDIV("class","ContentEditFull",$featPreview);
		ClosedDIV("class","ContentInfoFoot","End of $filename");
	}


}

## If this feature was moved to the FILTERED step, we need to make this into a file that is compatible with the VMS Systems.
## This will take the Merl Markup value found in the TMP file and add it to the correct feature sections.
## Other substitutions happen here that are only relevant to the MERL markup file, like adding <EP>, hidden and EOF markup.
## double quotes are converted to `` and '' for opening and closing quotes. 
## HTML markup styles are either converted to MERL markup styles or removed if it's not relevant. 
## There's also a function to reduce line size to 180 or less characters. 
## This file is copied to the DATE/POSTED directory. These files will NOT show up in the featureman main page to be edited. 

if ($newstatParam eq "Filtered") {

	my @cgiListNames = getTmpNameList($thistmp);
	makeadir($date,"Posted");
	$completeAction = "Filtered to Becky.";		
		if ($checkRecycle eq "TRUE") {
			copy($newfeat,$RecycleDir);
		}

	#open FH, "<", $newfeat; #Get existing feature and put all together to grab text between name tags
	open FH, "<:encoding(UTF-8)", $newfeat; #Get existing feature and put all together to grab text between name tags
	my @records = <FH>;
	my $allrecords = join "", @records;	
	close FH;
if (($thistmp =~ /cross.tmp$/) || ($thistmp =~ /puzz.tmp$/)) {
	open FMERL,">",$filterfeat;
	#print FMERL "Before Filter:\n\n$allrecords\n\n";
		foreach my $CGIlist (@cgiListNames) {
		if ($CGIlist eq "EP") {
			print FMERL "<ep>\n";
		} elsif ($CGIlist eq "EOF") {
			print FMERL "<2><4><30>\n";
		} elsif (($CGIlist =~ m/^Hidden/) || ($CGIlist eq "Hidden")) {
			my $markup = getTmpColValue($thistmp,$CGIlist);
			chomp($markup);
			print FMERL "$markup<ep>\n";
		} elsif (($CGIlist eq "Notes") || ($CGIlist eq "Photo")) {
			# We don't want Notes in the final product.	
		} else {
			my @allLines180;
			my @lineValues = getTMPLinevalues($thistmp,$CGIlist);
			my $markup = $lineValues[2];
			#my $findOpt = $lineValues[4];
			#my $markup = getTmpColValue($thistmp,$CGIlist);
			chomp($markup);
			#chomp($findOpt);
			$allrecords =~ /\<$CGIlist\>(.*)\<\/$CGIlist\>/; 
			my $this_line = $1;
			if ($this_line ne "") {
				my $quotesLine = convertQuotes($this_line);
				my $merlline = htmltomerlMarkup($quotesLine);
				#my $final_line = $merlline;
				#$final_line = make180($merlline);
				my $line180 = "$markup";
				my @each_line = split('\|\|',$merlline);
				foreach (@each_line) {
						my $line2add = make180($_);
						if ($line2add ne '') {
						if ($line2add =~ /^\d+\./) {
								$line2add =~ s/\.\s{2,}/\.\t/g;
								#$line2add =~ s/\.\s+/\.\t/g;
						}	
							if ($line2add =~ /^\d\./) {
								$line2add = "  $line2add";							
							}
						$line180 = "$line180${line2add}<ep>\n";
						}
				}
				print FMERL "$line180";
			}
		}
	}
	close FMERL;
} else {
	open FMERL,">",$filterfeat;
	#print FMERL "Before Filter:\n\n$allrecords\n\n";
		foreach my $CGIlist (@cgiListNames) {
		if ($CGIlist eq "EP") {
			print FMERL "<ep>\n";
		} elsif ($CGIlist eq "EOF30") {
			print FMERL "<30>\n";
		} elsif ($CGIlist eq "EOF") {
			print FMERL "<2><4><30>\n";
		} elsif (($CGIlist =~ m/^Hidden/) || ($CGIlist eq "Hidden")) {
			my $markup = getTmpColValue($thistmp,$CGIlist);
			chomp($markup);
			print FMERL "$markup<ep>\n";
		} elsif (($CGIlist eq "Notes") || ($CGIlist eq "Photo")) {
			# We don't want Notes in the final product.	
		} else {
			my @allLines180;
			my @lineValues = getTMPLinevalues($thistmp,$CGIlist);
			my $markup = $lineValues[2];
			#my $findOpt = $lineValues[4];
			#my $markup = getTmpColValue($thistmp,$CGIlist);
			chomp($markup);
			#chomp($findOpt);
			$allrecords =~ /\<$CGIlist\>(.*)\<\/$CGIlist\>/; 
			my $this_line = $1;
			if ($this_line ne "") {
				my $quotesLine = convertQuotes($this_line);
				my $merlline = htmltomerlMarkup($quotesLine);
				#my $final_line = $merlline;
				#$final_line = make180($merlline);
				my $line180 = "$markup";
				my @each_line = split('\|\|',$merlline);
				foreach (@each_line) {
						my $line2add = make180($_);
						if ($line2add ne '') {
							$line180 = "$line180${line2add}<ep>\n";
						}
						if (($line2add eq '') && (($thistmp =~ /cnot.tmp$/) || ($thistmp =~ /filmog.tmp$/) || ($thistmp =~ /tastytv.tmp$/))) {
							$line180 = "$line180<ep>\n";
						}

				}
				print FMERL "$line180";
			}
		}
	}
	close FMERL;

}

	## uploads finished feature to the WIRE2 directory on the VMS system
		if ($checkTest eq "LIVE") {
			uploadFeatureLIVE($filterfeat);
			uploadFeatureTEST($filterfeat);
			$completeAction = "Feature has been Filtered to Becky.";
		} else {
			uploadFeatureTEST($filterfeat);
			$completeAction = "Feature has been Filtered to Becky. <br>This feature is in Testing mode.\n Filtered to becky's TEST area for review.\n";
		}
		emailnotifier($oldstate,"posted",$filterfeat,$featName,$specFile);
		if ($oldstate eq 'Filtered') {
		emailnotifier($oldstate,"Refiltered",$filterfeat,$featName,$specFile);		
		}
		ClosedDIV("class","ContentInfo","Action Completed!<br>$completeAction");
		ClosedDIV("class","ContentEditFull",$featPreview);
		ClosedDIV("class","ContentInfo","End of $filename");
} 
if ($oldstate ne $newstatParam) {
	emailnotifier($oldstate,$newstatParam,$newfeat,$featName,$specFile);
	if ($newstatParam eq "Copy Edit") {
		CopyEditnotifier($oldstate,$newstatParam,$newfeat,$featName,$specFile);
	}
}
EndDIV();
OpenDIV("ID","Sidebar");
ClosedDIV("class","SidebarTitle","Return to Main page");
OpenDIV("class","SidebarGroup");
ClosedDIV("class","SidebarChoice","<a href=\"http://$homeIP/cgi-bin/FE2/featuremanager.cgi\"><button>Main Page</button></a>");
if ($prevFilter ne "") {
	ClosedDIV("class","SidebarTitle","Return to previous filter");
	ClosedDIV("class","SidebarChoice","<a href=\"$prevFilter\"><button>Previous Filter</button></a>");
}
EndDIV();
ClosedDIV("class","SidebarTitle","Edit $storyName now");
if (($CanCopy eq "TRUE") && ($newstatParam eq "copy")) {
	OpenDIV("class","SidebarGroup");
	if (($oldstate ne "reset") && ($oldstate ne "trash") && ($oldstate ne "preview")) {
		ClosedDIV("class","SidebarChoice","<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\"><input type=\"hidden\" name=\"tmp\" value=\"$copyTmp\"><input type=\"hidden\" name=\"fileLoc\" value=\"$copyFile\"><input type=\"hidden\" name=\"status\" value=\"In Progress\"><input type=\"hidden\" name=\"story\" value=\"$storyName\"><input type=\"submit\" value=\"Edit $storyName\"></form>");
		#<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\"><input type=\"hidden\" name=\"tmp\" value=\"$thistmp\"><input type=\"hidden\" name=\"fileLoc\" value=\"$featfile\"><input type=\"hidden\" name=\"status\" value=\"$newstatParam\"><input type=\"hidden\" name=\"story\" value=\"$storyname\"><input type=\"submit\" value=\"Open $lFile\"></form>"
	}
EndDIV();
} else {
ClosedDIV("class","SidebarTitle","Continue Editing this Feature");
	OpenDIV("class","SidebarGroup");
	if (($oldstate ne "reset") && ($oldstate ne "trash") && ($oldstate ne "preview")) {
		ClosedDIV("class","SidebarChoice","<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\"><input type=\"hidden\" name=\"tmp\" value=\"$thistmp\"><input type=\"hidden\" name=\"fileLoc\" value=\"$featfile\"><input type=\"hidden\" name=\"status\" value=\"$newstatParam\"><input type=\"hidden\" name=\"story\" value=\"$filename\"><input type=\"submit\" value=\"Return to editing $filename\"></form>");
		#<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\"><input type=\"hidden\" name=\"tmp\" value=\"$thistmp\"><input type=\"hidden\" name=\"fileLoc\" value=\"$featfile\"><input type=\"hidden\" name=\"status\" value=\"$newstatParam\"><input type=\"hidden\" name=\"story\" value=\"$storyname\"><input type=\"submit\" value=\"Open $lFile\"></form>"
	}
EndDIV();

}
=begin functions not ready yet.
if ($newstatParam eq "Filtered") {
	OpenDIV("class","SidebarGroup");
		if (($oldstate ne "reset") && ($oldstate ne "trash") && ($oldstate ne "preview")) {
		ClosedDIV("class","SidebarTitle","Create into a web page");
			ClosedDIV("class","SidebarChoice","<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/htmlmaker.cgi\">
			<input type=\"hidden\" name=\"spec\" value=\"$specFile\">
			<input type=\"hidden\" name=\"tmp\" value=\"$thistmp\">
			<input type=\"hidden\" name=\"fileLoc\" value=\"$featfile\">
			<input type=\"hidden\" name=\"story\" value=\"$filename\"><input type=\"submit\" value=\"Make Into Web Page\"></form>");
	#<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\"><input type=\"hidden\" name=\"tmp\" value=\"$thistmp\"><input type=\"hidden\" name=\"fileLoc\" value=\"$featfile\"><input type=\"hidden\" name=\"status\" value=\"$newstatParam\"><input type=\"hidden\" name=\"story\" value=\"$storyname\"><input type=\"submit\" value=\"Open $lFile\"></form>"
	}
	EndDIV();
}
=cut not ready for primetime

if (($CanCopy eq "TRUE") && ($newstatParam ne "copy")) {
		if (($oldstate ne "reset") && ($oldstate ne "trash") && ($oldstate ne "preview")) {
		my $CopyTo = $GetFeatSpecs{'copy'};
		my $copyCheck = checkforFeat("$CopyTo.$date");
		my $copyFile = "$FeatFolder/$date/In Progress/$CopyTo.$date";
		my $newFileLoc = "$FeatFolder/$date/Filtered/$storyName";
		my $copyTMP = "$CopyTo.$date";
		ClosedDIV("class","SidebarTitle","Copy $featName.$date to $CopyTo.$date");
		OpenDIV("class","SidebarGroup");
		if ($copyCheck ne "TRUE") {
			ClosedDIV("class","SidebarChoice","<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/FF_mover.cgi\"><input type=\"hidden\" name=\"tmp\" value=\"$thistmp\"><input type=\"hidden\" name=\"fileLoc\" value=\"$newfeat\"><input type=\"hidden\" name=\"newstate\" value=\"copy\"><input type=\"hidden\" name=\"story\" value=\"$CopyTo.$date\"><input type=\"submit\" value=\"Copy to $CopyTo.$date\"></form>");
		} else {
			ClosedDIV("class","SidebarChoice","Copy not available for $CopyTo.$date. Feature already exists.");
		}
		#<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\"><input type=\"hidden\" name=\"tmp\" value=\"$thistmp\"><input type=\"hidden\" name=\"fileLoc\" value=\"$featfile\"><input type=\"hidden\" name=\"status\" value=\"$newstatParam\"><input type=\"hidden\" name=\"story\" value=\"$storyname\"><input type=\"submit\" value=\"Open $lFile\"></form>"
	}
	EndDIV();
}
if ($oldstate eq "preview") {
OpenDIV("class","SidebarGroup");
	ClosedDIV("class","SidebarTitle","Continue Editing this Feature");
	ClosedDIV("class","SidebarChoice","<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\"><input type=\"hidden\" name=\"tmp\" value=\"$thistmp\"><input type=\"hidden\" name=\"fileLoc\" value=\"$featfile\"><input type=\"hidden\" name=\"status\" value=\"$newstatParam\"><input type=\"hidden\" name=\"story\" value=\"$filename\"><input type=\"submit\" value=\"Open $filename for editing\"></form>");
	#<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\"><input type=\"hidden\" name=\"tmp\" value=\"$thistmp\"><input type=\"hidden\" name=\"fileLoc\" value=\"$featfile\"><input type=\"hidden\" name=\"status\" value=\"$newstatParam\"><input type=\"hidden\" name=\"story\" value=\"$storyname\"><input type=\"submit\" value=\"Open $lFile\"></form>"
EndDIV();
}

	ClosedDIV("class","SidebarTitle","Go to Deadline Manager");

OpenDIV("class","SidebarGroup");
	print "<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/featureDeadlines.cgi\">\n";
	ClosedDIV("class","SidebarChoice","<input type=\"submit\" name=\"actionDo\" value=\"Go to Deadline Manager.\">");
	print "</form>\n";
EndDIV();

EndDIV();

EndDIV();
HTMLend();
