#! /usr/bin/perl
##########################################
#
#	by Larry Gonyea
#      Gracenote
#  The Feature_Editor script creates new features as well as opens existing features.
#  It takes information from the template file to determine the field type and field name
#  If this is opening a feature already started, it will display information from the feature within the fieldname tags and place it in the correct form fields.
#  
###############################################
use strict;
#use warnings;
use Tie::File;
use File::Copy;
use CGI;
use utf8;
use encoding 'UTF-8';
require("FF_common_func.cgi");
require("FF_web_elements.cgi");
#my $baseFEfolder = "/Library/WebServer/CGI-Executables/FE2";
#my $FeatFolder = "/Library/WebServer/FF2";
my ($baseFEfolder,$FeatFolder) = getFilesLocal();
my $prevFilter;
my $CanCopy;
my $copyTmp;
my ($homeIP,$systemType) = getHomeAddress();
my $selfPage = "http://$homeIP/cgi-bin/FE2/feature_editor.cgi";
my ($fieldType,$fieldName,$fieldMarkup,$fieldText);
my @statelist = getstatelist();
my $homeDir = "$FeatFolder/";
my $templateDir = "$baseFEfolder/templates/";
my $specDir = "$baseFEfolder/specs/";
my $liveList = "$baseFEfolder/liveFeatList.txt";
## CGI PARAMS
my $query = new CGI;
my $thisfile = $query->param('fileLoc');
my $statParam = $query->param('status');
my $thisstory = $query->param('story');
my $viewStyle = $query->param('viewtype');
$prevFilter = $query->param('backlink');
my $mod_time = $query->param('modtime');
## NECESSARY STRINGS
#$thisfile = "$thisfile$thisstory";
#$thisfile = "$thisfile";
my @storyparts = split(/\./,$thisstory);
my $storyname = $storyparts[0];
my $thistmp = "${storyname}.tmp";
my $specFile = "${specDir}${storyname}.spc";
my %FeatSpecs = hashAFile($specFile);
my $checkCopy = $FeatSpecs{'copy'};
if ($checkCopy ne "") {
 $CanCopy = "TRUE";
} else {
 $CanCopy = "FALSE"; 
}

my $fieldOption;
my $FeatStatus = $FeatSpecs{'status'};
if ($FeatStatus eq "live") {
	$FeatStatus = "Live";
} else {
	$FeatStatus = "Test";
}
my $NotesOnTheSide = "";
my $PhotoOnTheSide = "";
my $featureFile = "$FeatFolder/Temp/$statParam/$thisstory";
my $templatefile = "${templateDir}${storyname}.tmp";
my @storyparts = split(/\./,$thisstory);
my $storyname = $storyparts[0];
my $featdate = $storyparts[1];

## BEGIN BUILDING WEBPAGE
makeHTML5type();
LoadCSS();
LoadJS();
JQfadeIn("#Content","slow");

HTMLtitle("Gracenote Feature Writer");

OpenDIV("ID","Header","");

if ($viewStyle eq "ViewOnly") {
	makeHeaderTopper();
} else {
	ClosedDIV("class","HeaderTopper","Gracenote Features Editor");
}
ClosedDIV("class","HeaderLeft","Gracenote Features Editor");
EndDIV();
OpenDIV("ID","Nav");
## Create the rop down lists for filtering features.
OpenDIV("class","NavLeftNotUL","This story is $FeatStatus.");
#print "$FeatSpecs{'name'} is due on $FeatSpecs{'dueday'} at $FeatSpecs{'duetime'} for $FeatSpecs{'dueweek'}";
EndDIV();
my $weekDue = getweeksout("$FeatSpecs{'dueweek'}");
OpenDIV("class","NavRight","$FeatSpecs{'name'}.$weekDue is due on $FeatSpecs{'dueday'} at $FeatSpecs{'duetime'}");
EndDIV();
EndDIV();


OpenDIV("ID","Container");


#If this is a new feature make a new feature with blank fields.
# if there's a default text in the TMP file, it wil add that to the correct field.
OpenDIV("ID","Content");

if ($statParam eq "new") { 
ClosedDIV("class","ContentInfo","<center><h1><b>Currently editing $thisstory </b></h1></center>");
ClosedDIV("class","clearFloat","");

	print "<form id=\"Mover\" method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/FF_mover.cgi\" accept-charset=\"utf-8\">\n";
	my $featureFile = "$FeatFolder/$featdate/In Progress/$thisstory";
	print "<input type=\"hidden\" name=\"backlink\" value=\"$prevFilter\">";
	print "<input type=\"hidden\" name=\"fileLoc\" value=\"$featureFile\">";
	#my $templatefile = "${templateDir}${storyname}.tmp";

	print "<input type=\"hidden\" name=\"tmp\" value=\"$templatefile\">";
	open FH,"<:encoding(UTF-8)",$templatefile or die $!;
	my @fieldlists = <FH>;
	close(FH);

		foreach my $line (@fieldlists) {
			my @featfield = split('\|',$line);
 			my $fieldName = $featfield[0];
 			my $fieldType = $featfield[1];
 			my $fieldMarkup = $featfield[2];
 			my $fieldText = $featfield[3];
 			my $fieldOption = $featfield[4];
 			chomp($fieldOption);
 			if ($fieldName eq "Notes") {
 				$NotesOnTheSide = "$fieldText";
				my $showNotes = $fieldText;
 			}
 			if ($fieldName eq "Photo") {
 				$PhotoOnTheSide = "$fieldText";
				my $showPhoto = $fieldText;
 			}

 		if (($fieldName ne "EOF") && ($fieldName ne "Notes") && ($fieldName ne "Photo")) {
 			if (($fieldType eq "static") && ($fieldName eq "Name")) {
 				OpenDIV("class","ContentForm");
 				ClosedDIV("class","ContentFormName","$fieldName$fieldOption");
				ClosedDIV("class","ContentFormField","<input type=\"$fieldType\" size=\"100%\" name=\"$fieldName\" value='$thisstory\' readonly autofocus>");
				EndDIV();
			 } elsif ($fieldType eq "text") {
 				OpenDIV("class","ContentForm");
 				ClosedDIV("class","ContentFormName","$fieldName$fieldOption");
				utf8::encode($fieldText);
				$fieldText = $query->escapeHTML($fieldText);
				ClosedDIV("class","ContentFormField","<textarea rows=\"2\" cols=\"110\" name=\"$fieldName\">$fieldText</textarea>");
				EndDIV();
			} elsif ($fieldType eq "shorttext") {
 				OpenDIV("class","ContentForm");
 				ClosedDIV("class","ContentFormName","$fieldName$fieldOption");
				$fieldText = $query->escapeHTML($fieldText);
				ClosedDIV("class","ContentFormField","<textarea rows=\"1\" cols=\"110\" name=\"$fieldName\">$fieldText</textarea>");
				EndDIV();
			} elsif ($fieldType eq "ckeditor") {
 				OpenDIV("class","ContentForm");
 				ClosedDIV("class","ContentFormName","$fieldName$fieldOption");
				ClosedDIV("class","ContentFormField","<textarea rows=\"15\" class=\"$fieldType\" name=\"$fieldName\">$fieldText</textarea>");
				EndDIV();
			} elsif ($fieldType eq "static") {
				OpenDIV("class","ContentForm");
 				ClosedDIV("class","ContentFormName","$fieldName$fieldOption");
				$fieldText = $query->escapeHTML($fieldText);
				ClosedDIV("class","ContentFormName","<input type=\"text\" name=\"$fieldName\" value=\'$fieldText\' readonly>");
				EndDIV();
			}
		}
	}

#If this is not a new feature, this opens and existing feature.
# This will move the feature to the TEMP area then place each tagged section into the matching for field. 
# At this point, the default text is not grabbed from within the TMP file, it has already been written to the feature. Any changes to the default text
#       Should be reflected when it's reopened. 
#  Here we also call the mover script to take the correct action based on the step selected.
		
} elsif ($viewStyle eq "ViewOnly") {
	ClosedDIV("class","ContentInfo","<b>Currently previewing $thisstory<br>Current status is $statParam.</b>");
	my @storyparts = split(/\./,$thisstory);
	my $storyname = $storyparts[0];
	my $featdate = $storyparts[1];
	my $OrigFile = "$FeatFolder/$featdate/$statParam/$thisstory";
	#my $templatefile = "${templateDir}${storyname}.tmp";
	my $featureFile = "$FeatFolder/$featdate/$statParam/$thisstory";
	my $featPreview = MakeAPreview($templatefile,$OrigFile,$storyname);
	ClosedDIV("class","ContentEditFull","$featPreview");
	$NotesOnTheSide = findNotes($featureFile);
	$PhotoOnTheSide = findPhoto($featureFile);

} elsif ($viewStyle eq "recycle") {
# story=spoquiz
# fileLoc=features10192014.xml
# status=recycle
# pageType=recycle
# Mode=recycle
#my $thisfile = $query->param('fileLoc');
#my $statParam = $query->param('status');
#my $thisstory = $query->param('story');
#my $viewStyle = $query->param('viewtype');
##my $thistmp = "${storyname}.tmp";
#my $specFile = "${specDir}${storyname}.spc";
	#my $templatefile = "${templateDir}${storyname}.tmp";


ClosedDIV("class","ContentInfo","<center><h1><b>Currently editing $thisstory </b></h1></center>");
ClosedDIV("class","clearFloat","");
	my $featureFile = "$FeatFolder/$featdate/In Progress/$thisstory";
	my $templateFile = "$baseFEfolder/templates/$thistmp";
		my $openXML = "$thisfile";
	$statParam = "new";
	#print "<form method=\"post\" id=\"Mover\" action=\"http://$homeIP/cgi-bin/FE2/FF_mover.cgi\">\n";
#	print "<form method=\"post\" id=\"Mover\" action=\"http://$homeIP/cgi-bin/FE2/FF_mover.cgi\" accept-charset=\"utf-8\">\n";
	print "<form method=\"post\" id=\"Mover\" action=\"http://$homeIP/cgi-bin/FE2/FF_mover.cgi\" accept-charset=\"utf-8\">\n";
	print "<input type=\"hidden\" name=\"fileLoc\" value=\"$featureFile\">";
	print "<input type=\"hidden\" name=\"tmp\" value=\"$templatefile\">";
	#print "<input type=\"hidden\" name=\"backlink\" value=\"$prevFilter\">";

		#ClosedDIV("class","ContentInfo","Doing this xml $xmlDir$fileToDo<br> Looking for this feature $xmlFeat<br>");
				open FH, "<", $openXML; #Get 
				my @records = <FH>;
				my $allrecords = join "", @records;	
				my $fieldCheck = $allrecords;
				close FH;
				$allrecords =~  /\<$storyname\>(.*)\<\/$storyname\>/s;
				my $thisFeat = $1;

		open TH,"<:encoding(UTF-8)",$templateFile or die $!;
		my @fieldlists = <TH>;
		close(TH);
		#my $wholeFeat;
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
 		if (($fieldName ne "EOF") && ($fieldName ne "Notes") && ($fieldName ne "Photo")) {
 			if (($fieldType eq "static") && ($fieldName eq "Name")) {
 				#$fieldText = $query->escapeHTML($fieldText);
							$fieldText =~ s/\n/\<br\>/g;
				OpenDIV("class","ContentForm");
 				ClosedDIV("class","ContentFormName","$fieldName");
				ClosedDIV("class","ContentFormField","<input type=\"text\" rows=\"1\" cols=\"200\" name=\"$fieldName\" value=\'$thisstory\' readonly autofocus>");
				EndDIV();
			 } elsif ($fieldType eq "shorttext") {
 				utf8::encode($fieldText);
				#$fieldText = $query->escapeHTML($fieldText);
				OpenDIV("class","ContentForm");
 				ClosedDIV("class","ContentFormName","$fieldName");
				ClosedDIV("class","ContentFormField","<textarea rows=\"1\" cols=\"110\" name=\"$fieldName\">$fieldText</textarea>");
				EndDIV();
			} elsif ($fieldType eq "text") {
			 	#utf8::encode($fieldText);
				#$fieldText = $query->escapeHTML($fieldText);
				OpenDIV("class","ContentForm");
 				ClosedDIV("class","ContentFormName","$fieldName");
				ClosedDIV("class","ContentFormField","<textarea rows=\"2\" cols=\"110\" name=\"$fieldName\">$fieldText</textarea>");
				EndDIV();
			} elsif ($fieldType eq "ckeditor") {
				$fieldText =~ s/\n/\<br\>/g;
				OpenDIV("class","ContentForm");
 				ClosedDIV("class","ContentFormName","$fieldName");
				ClosedDIV("class","ContentCKField","<textarea class=\"ckeditor\" name=\"$fieldName\">$fieldText</textarea>");
				EndDIV();
			} elsif ($fieldType eq "static") {
				#$fieldText = $query->escapeHTML($fieldText);
 				OpenDIV("class","ContentForm");
 				ClosedDIV("class","ContentFormName","$fieldName");
				ClosedDIV("class","ContentFormField","<textarea readonly rows=\"2\" cols=\"110\" name=\"$fieldName\">$fieldText</textarea>");
				EndDIV();
			}
		}
	}

} else { 

ClosedDIV("class","ContentInfo","<b>Currently editing $thisstory</b>");
ClosedDIV("class","clearFloat","");

	print "<form method=\"post\" id=\"Mover\" action=\"http://$homeIP/cgi-bin/FE2/FF_mover.cgi\" accept-charset=\"utf-8\">\n";
	my @storyparts = split(/\./,$thisstory);
	my $storyname = $storyparts[0];
	my $featdate = $storyparts[1];
	my $OrigFile = "$FeatFolder/$featdate/$statParam/$thisstory";
	my $featureFile = "$FeatFolder/Temp/$statParam/$thisstory";
	move($OrigFile,$featureFile);
	print "<input type=\"hidden\" name=\"backlink\" value=\"$prevFilter\">";
	print "<input type=\"hidden\" name=\"fileLoc\" value=\"$featureFile\">";
	print "<input type=\"hidden\" name=\"tmp\" value=\"$templatefile\">";
		open FH, "<:encoding(UTF-8)", $featureFile; #Get existing feature and put all together to grab text between name tags
		my @records = <FH>;
		my $allrecords = join "", @records;	
		my $fieldCheck = $allrecords;
		close FH;
	open TH,"<:encoding(UTF-8)",$templatefile or die $!;
	my @fieldlists = <TH>;
		close(TH);

		foreach my $line (@fieldlists) {
			my @featfield = split('\|',$line);
 			my $fieldName = $featfield[0];
 			my $fieldType = $featfield[1];
 			my $fieldMarkup = $featfield[2];
 			my $fieldOption = $featfield[4];
 			chomp($fieldOption);

 			$allrecords =~ /\<$fieldName\>(.*)\<\/$fieldName\>/s; 
			my $fieldText = $1;
			
			if ($fieldCheck !~ /<$fieldName>/s) {
				my $fieldText = "";
			}


 			 if ($fieldName eq "Notes") {
 			  	$NotesOnTheSide = "$fieldText";
 				my $showNotes = $fieldText;
 			}
 			  if ($fieldName eq "Photo") {
 			  	$PhotoOnTheSide = "$fieldText";
 				my $showPhoto = $fieldText;
 			}
 		if (($fieldName ne "EOF") && ($fieldName ne "Notes") && ($fieldName ne "Photo")) {
 			if (($fieldType eq "static") && ($fieldName eq "Name")) {
 				$fieldText = $query->escapeHTML($fieldText);
				OpenDIV("class","ContentForm");
 				ClosedDIV("class","ContentFormName","$fieldName");
				ClosedDIV("class","ContentFormField","<input type=\"text\" rows=\"1\" cols=\"200\" name=\"$fieldName\" value=\'$thisstory\' readonly autofocus>");
				EndDIV();
			 } elsif ($fieldType eq "shorttext") {
 				utf8::encode($fieldText);
				$fieldText = $query->escapeHTML($fieldText);
				OpenDIV("class","ContentForm");
 				ClosedDIV("class","ContentFormName","$fieldName");
				ClosedDIV("class","ContentFormField","<textarea rows=\"1\" cols=\"110\" name=\"$fieldName\">$fieldText</textarea>");
				EndDIV();
			} elsif ($fieldType eq "text") {
			 	utf8::encode($fieldText);
				$fieldText = $query->escapeHTML($fieldText);
				OpenDIV("class","ContentForm");
 				ClosedDIV("class","ContentFormName","$fieldName");
				ClosedDIV("class","ContentFormField","<textarea rows=\"2\" cols=\"110\" name=\"$fieldName\">$fieldText</textarea>");
				EndDIV();
			} elsif ($fieldType eq "ckeditor") {
				OpenDIV("class","ContentForm");
 				ClosedDIV("class","ContentFormName","$fieldName");
				ClosedDIV("class","ContentCKField","<textarea class=\"ckeditor\" name=\"$fieldName\">$fieldText</textarea>");
				EndDIV();
			} elsif ($fieldType eq "static") {
				$fieldText = $query->escapeHTML($fieldText);
 				OpenDIV("class","ContentForm");
 				ClosedDIV("class","ContentFormName","$fieldName");
				ClosedDIV("class","ContentFormField","<textarea readonly rows=\"2\" cols=\"110\" name=\"$fieldName\">$fieldText</textarea>");
				EndDIV();
			}
		}
	}
} #end open existing feature

ClosedDIV("class","ContentInfoFoot","End of $thisstory");

EndDIV();
OpenDIV("ID","Sidebar");

if ($viewStyle ne "ViewOnly") {
	my $oldstate = $statParam;
ClosedDIV("class","SidebarTitle","Notes");
OpenDIV("class","SidebarGroup");
	$NotesOnTheSide =~ s/\<br\>/\n/g;
	ClosedDIV("class","ContentFormField","<textarea rows=\"10\" name=\"Notes\">$NotesOnTheSide</textarea>");
EndDIV();
my	$checkPhoto = CheckforPhoto($templatefile);
if ($checkPhoto eq "Yes" ) {
ClosedDIV("class","SidebarTitle","Photo Info");
OpenDIV("class","SidebarGroup");
	$PhotoOnTheSide =~ s/\<br\>/\n/g;
	#if ($PhotoOnTheSide eq "") {
	#	$PhotoOnTheSide = "No photo information supplied yet.";
	#	}
	ClosedDIV("class","ContentFormField","<textarea rows=\"10\" name=\"Photo\">$PhotoOnTheSide</textarea>");
EndDIV();
}
	print "</form>\n";
ClosedDIV("class","SidebarTitle","Save and change status to Feature");
OpenDIV("class","SidebarGroup");
	print "<input type=\"hidden\" name=\"oldstate\" form=\"Mover\" value=\"$oldstate\">";
	#my $statelist = makeStateDropdown($statParam);
	my $statelist = makeStateRadio($statParam);
	print "$statelist";
	#ClosedDIV("class","SidebarRadio","$statelist");

	#ClosedDIV("class","SidebarNothing","<select name=\"newstate\">\n$statelist</select>");
	ClosedDIV("class","SidebarChoice","<input type=\"submit\" form=\"Mover\" name=\"actionDo\" value=\"Submit $thisstory\">");
	#print "</form>\n";
EndDIV();
	ClosedDIV("class","SidebarTitle","Quit $thisstory");

OpenDIV("class","SidebarGroup");	
	print "<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/FF_mover.cgi\">\n";
	print "<input type=\"hidden\"  name=\"backlink\" value=\"$prevFilter\">";
	print "<input type=\"hidden\" name=\"tmp\" value=\"$templatefile\">";
	print "<input type=\"hidden\" name=\"oldstate\" value=\"$statParam\">";
#	print "<input type=\"hidden\" name=\"oldstate\" value=\"new\">";
	print "<input type=\"hidden\" name=\"newstate\" value=\"reset\">";
	print "<input type=\"hidden\"  name=\"fileLoc\" value=\"$featureFile\">";
	print "<input type=\"hidden\" name=\"story\" value=\"$thisstory\">";
	ClosedDIV("class","SidebarChoice","<input type=\"submit\" name=\"actionDo\" value=\"Quit without saving\">");
	print "</form>\n";
EndDIV();

if ($statParam ne "new") {
#		ClosedDIV("class","SidebarTitle","Delete Feature");
#		OpenDIV("class","SidebarGroup");
#		print "<form onsubmit=\"return confirm('Please confirm that you want to delete: $thisstory.')\;\" method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/FF_mover.cgi\">\n";
#		print "<input type=\"hidden\" name=\"tmp\" value=\"$templatefile\">";
#		print "<input type=\"hidden\" name=\"oldstate\" value=\"trash\">";
#		print "<input type=\"hidden\" name=\"newstate\" value=\"trash\">";
#		print "<input type=\"hidden\" name=\"fileLoc\" value=\"$featureFile\">";
#		print "<input type=\"hidden\" name=\"story\" value=\"$thisstory\">";
#				ClosedDIV("class","SidebarChoice","<input type=\"submit\" value=\"Delete $thisstory\">");
#		print "</form>\n";
#		EndDIV();
	}
	
} else {

ClosedDIV("class","SidebarTitle","notes");
if ($NotesOnTheSide eq "") {
$NotesOnTheSide = "No notes for $thisstory";
}
OpenDIV("class","SidebarGroup");
	ClosedDIV("class","NotesField","$NotesOnTheSide");
EndDIV();
my $checkPhoto = CheckforPhoto($templatefile);
if ($checkPhoto eq "Yes" ) {
	if ($PhotoOnTheSide eq "") {
		$PhotoOnTheSide = "No photo information supplied yet.";
		}
	ClosedDIV("class","SidebarTitle","Photo");
	OpenDIV("class","SidebarGroup");
	ClosedDIV("class","NotesField","$PhotoOnTheSide");
	EndDIV();
}
	print "</form>\n";

ClosedDIV("class","SidebarTitle","Open $thisstory for editing");
OpenDIV("class","SidebarGroup");
	print "<form method=\"get\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\">";
	print "<input type=\"hidden\" name=\"tmp\" value=\"$templatefile\">";
	print "<input type=\"hidden\" name=\"modtime\" value=\"$mod_time\">";
	print "<input type=\"hidden\" name=\"fileLoc\" value=\"$thisfile\">";
	print "<input type=\"hidden\" name=\"status\" value=\"$statParam\">";
	print "<input type=\"hidden\" name=\"story\" value=\"$thisstory\">";
	print "<input type=\"hidden\" name=\"viewtype\" value=\"Edit\">";
	ClosedDIV("class","SidebarChoice","<input type=\"submit\" name=\"actionDo\" value=\"Edit $thisstory\">");
	print "</form>\n";
EndDIV();
	ClosedDIV("class","SidebarTitle","Return to main page");

OpenDIV("class","SidebarGroup");
	print "<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/featuremanager.cgi\">\n";
	ClosedDIV("class","SidebarChoice","<input type=\"submit\" name=\"actionDo\" value=\"Return to main page.\">");
	print "</form>\n";
EndDIV();
	ClosedDIV("class","SidebarTitle","Go to Deadline Manager");

OpenDIV("class","SidebarGroup");
	print "<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/featureDeadlines.cgi\">\n";
	ClosedDIV("class","SidebarChoice","<input type=\"submit\" name=\"actionDo\" value=\"Go to Deadline Manager.\">");
	print "</form>\n";
EndDIV();

#if ($statParam ne "new") {
#	ClosedDIV("class","SidebarTitle","Delete Feature");
#
#	OpenDIV("class","SidebarGroup");
#		print "<form onsubmit=\"return confirm('Please confirm that you want to delete: $thisstory.')\;\" method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/FF_mover.cgi\">\n";
#		print "<input type=\"hidden\" name=\"tmp\" value=\"$templatefile\">";
#		print "<input type=\"hidden\" name=\"oldstate\" value=\"trash\">";
#		print "<input type=\"hidden\" name=\"newstate\" value=\"trash\">";
#		print "<input type=\"hidden\" name=\"fileLoc\" value=\"$thisfile\">";
#		print "<input type=\"hidden\" name=\"story\" value=\"$thisstory\">";
#		ClosedDIV("class","SidebarChoice","<input type=\"submit\" value=\"Delete $thisstory\">");
#		print "</form>\n";
#	EndDIV();
#}

if (($CanCopy eq "TRUE") && ($statParam eq "Filtered")) {
		my $CopyTo = $FeatSpecs{'copy'};
		my $copyCheck = checkforFeat("$CopyTo.$featdate");
		my $copyFile = "$FeatFolder/$featdate/In Progress/$CopyTo.$featdate";
		my $newFileLoc = "$FeatFolder/$featdate/Filtered/$thisstory";
		my $copyTMP = "$baseFEfolder/templates/$storyname.tmp";
		my $newfeat = "$CopyTo.$featdate";
		ClosedDIV("class","SidebarTitle","Copy $thisstory to $CopyTo.$featdate");
		OpenDIV("class","SidebarGroup");
		if ($copyCheck ne "TRUE") {
			ClosedDIV("class","SidebarChoice","<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/FF_mover.cgi\"><input type=\"hidden\" name=\"tmp\" value=\"$copyTMP\"><input type=\"hidden\" name=\"fileLoc\" value=\"$newFileLoc\"><input type=\"hidden\" name=\"newstate\" value=\"copy\"><input type=\"hidden\" name=\"story\" value=\"$CopyTo.$featdate\"><input type=\"submit\" value=\"Copy to $CopyTo.$featdate\"></form>");
		} else {
			ClosedDIV("class","SidebarChoice","Copy not available for $CopyTo.$featdate. Feature already exists.");
		}
		#<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\"><input type=\"hidden\" name=\"tmp\" value=\"$thistmp\"><input type=\"hidden\" name=\"fileLoc\" value=\"$featfile\"><input type=\"hidden\" name=\"status\" value=\"$newstatParam\"><input type=\"hidden\" name=\"story\" value=\"$storyname\"><input type=\"submit\" value=\"Open $lFile\"></form>"
	EndDIV();
}


}
EndDIV();
EndDIV();

EndDIV();

HTMLend();