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
my $specDir = "$baseFEfolder/specs/";
my $histDir = "$baseFEfolder/BEHistory/";
my $trashDir = "${FeatFolder}/trash/";
my $tempDir = "$baseFEfolder/templates/";
my $userDir = "$baseFEfolder/users/";
my $specTemplate = "/Library/WebServer/CGI-Executables/FormTemplates/specTemplate.spc";
@specFiles = ArrayADir("$specDir","no");
my @specTempArray = arrayFile("$specTemplate");
#fileToDo should be only the feature name, no path or extension
my $fileToDo = $query->param('fileToDo');
# Mode is used to determine if we are going to edit, view, or save
my $pageMode = $query->param('Mode');
my $pageType = $query->param('pageType');


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

ClosedDIV("class","SidebarTitle","Recover Deleted Feature");
OpenDIV("class","SidebarGroup","","");
my $trashDirDrop = getFileList("$trashDir","Yes");
ClosedDIV("class","SidebarChoice","<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/FCM_Backend.cgi\"><select name=\"fileToDo\">\n$trashDirDrop</select><input type=\"hidden\" name=\"pageType\" value=\"recover\"><input type=\"hidden\" name=\"Mode\" value=\"move\"><input type=\"submit\" value=\"Recover Feature\"></form>\n");
#ClosedDIV("class","SidebarChoice","<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/FCM_Backend.cgi\"><input type=\"hidden\" name=\"pageType\" value=\"SpecEditor\"><input type=\"submit\" value=\"Show All Sepc Files\"></form>\n");
EndDIV();

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