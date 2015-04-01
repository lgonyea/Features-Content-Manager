#! /usr/bin/perl

#use warnings;
use strict;
use Tie::File;
use File::Copy;
use CGI;
use File::Find;
use utf8;
use encoding 'UTF-8';
require("FF_common_func.cgi");
require("FF_web_elements.cgi");
#my $baseFEfolder = "/Library/WebServer/CGI-Executables/FE2";
#my $FeatFolder = "/Library/WebServer/FF2";
my ($baseFEfolder,$FeatFolder) = getFilesLocal();
my ($dl_second, $dl_minute, $dl_hour, $dl_day, $dl_month, $dl_year, $dl_weekDay, $dl_dayOfYear, $IsDST) = localtime(time);
my ($homeIP,$systemType) = getHomeAddress();
#my $homeIP = "localhost";
my $thisstate = "";
my $selfPage = "$homeIP/cgi-bin/FE2/featureDeadlines.cgi";
my @daysOfWeek = qw( Sunday Monday Tuesday Wednesday Thursday Friday Saturday );
my @shortdaysOfWeek = qw( Sun Mon Tue Wed Thu Fri Sat );
my @monthsOfYear = qw( January Febuary March April May June July August September October November December );
my @shortmonthsOfYear = qw( Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec );
my $pageWeekday = $daysOfWeek[$dl_weekDay];
my @allsteps = getstatelist();
my @allbaseweeks = getweeks();
my $query = new CGI;
my $myweek = $query->param('deadlineweek');
$thisstate = $query->param('statefilter');
my $divHead;
if ($thisstate eq "") {
	$thisstate = "All";
}
my $currenttime = GetDateTime();
makeHTML5type();
LoadCSS();
LoadJS();
JQfadeIn("#Content","slow");

HTMLtitle("Gracenote Feature Deadline Tracker");

OpenDIV("ID","Header");
makeHeaderTopper();

ClosedDIV("class","HeaderLeft","Gracenote Feature Deadline Tracker");
#my $AllFeatList = getFileList("$baseFEfolder/templates","No");
EndDIV();

#start the navigation bar
OpenDIV("ID","Nav");
## Create the rop down lists for filtering features.
OpenDIV("class","NavLeft");

makeDLNAVbar();
EndDIV();
#OpenDIV("class","NavRight","");
#ClosedDIV("class","NavRight","<a href=\"http://$homeIP/cgi-bin/FE2/featuremanager.cgi\">FCM Editor</a>");
#ClosedDIV("class","NavRight","<a href=\"http://$homeIP/cgi-bin/FE2/FCM_Backend.cgi\">FCM Backend Manager</a>");

#EndDIV();
EndDIV();

###############


#############
#Begin building content area based on any filters applied
OpenDIV("ID","Container");

# Sidebar starts. This shows list of features available to create. 
# If a feature exists for that week, it is not shown in the drop down list for that week.
my $thisdl;
my $actionButton;
my @deadlinesThisWeek;
my $StartTally = 0;
my $NotStartTally = 0;
my $CompleteTally = 0;
if (($myweek eq "Today") || ($myweek eq "This Week")) {
	@deadlinesThisWeek = getFeatDeadlines("0");
} elsif ($myweek eq "Next Week") {
	@deadlinesThisWeek = getFeatDeadlines("1");
} else {
	my @deadlines1 = getFeatDeadlines("0");
	my @deadlines2 = getFeatDeadlines("1");
	my @deadlines3 = getFeatDeadlines("2");
	@deadlinesThisWeek = (@deadlines1,@deadlines2,@deadlines3);
}

OpenDIV("ID","Content");
OpenDIV("ID","DLpage");
my @valuesteps = ("In Progress","Unedited","Original Edit","Final Read","Ready For Production","Filtered");
my $ProgValue;
my $hashStep;
my $STvalue = 0;
my %steptovalue;
my $valStat;
my $key;
my $progStatus;
my $col1Info;
my @startedCol;
my @completeCol;
my @notStartedCol;
foreach $hashStep (@valuesteps) {
	$STvalue++;
	$steptovalue{$hashStep} = $STvalue; 
}
my $maxValue = $STvalue;
ClosedDIV("class","ContentInfo","$thisstate Features due $myweek");

foreach $thisdl (@deadlinesThisWeek) {
	my @deadlineparts = split('\|',$thisdl);
	my $dlStatus = $deadlineparts[0];
	my $dlName = $deadlineparts[1];
	my $dlDay = $deadlineparts[2];
	my $dlTime = $deadlineparts[3];
	my $dlState = $deadlineparts[4];
	my $lLink = $deadlineparts[5];
	my $file_time = $deadlineparts[6];
	my @getTMPname = split('\.',$dlName);
	my $tmp = "$baseFEfolder/templates/${getTMPname[0]}.tmp";
	my @StatusParts = split(' - ',$dlStatus);

	if ((($myweek eq "Today") && ($dlDay eq "Today")) && (($thisstate eq $StatusParts[0]) || ($thisstate eq "All")) || ((($thisstate eq $StatusParts[0]) || ($thisstate eq "All"))  && ($myweek ne "Today")))  {	
		if ($dlStatus eq "Not Started") {
			$progStatus = "Not Started";
			$valStat = "0";
			$NotStartTally++;
			$divHead = "DLHeadNS";
			if ($dlDay eq "Today") {
				$col1Info = "<b>$dlName</b> <hr>Due: ${dlDay} at $dlTime";
			} else {
				$col1Info = "<b>$dlName</b> <hr>Due: ${dlDay}s at $dlTime";
			}
			$actionButton = "<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\"><input type=\"hidden\" name=\"story\" value=\"$dlName\"><input type=\"hidden\" name=\"status\" value=\"new\"><input type=\"submit\" value=\"Start $dlName\"></form>\n";
			@notStartedCol = (@notStartedCol,"$progStatus|$valStat|$divHead|$col1Info|$actionButton");
#ClosedDIV("class","$divHead","${col1Info}<br>${actionButton}");
		} elsif ($StatusParts[0] eq "Started") {
			$StartTally++;
			$valStat = $StatusParts[1];		
			$divHead = "DLHeadST";
			if ($dlDay eq "Today") {
				$col1Info = "$dlName  <hr>Due: ${dlDay} at $dlTime<br>Last Modified:<br> $file_time";
			} else {
				$col1Info = "$dlName  <hr>Due: ${dlDay} at $dlTime<br>Last Modified:<br> $file_time";
			}
			$actionButton = "<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\"><input type=\"hidden\" name=\"tmp\" value=\"$tmp\"><input type=\"hidden\" name=\"modtime\" value=\"$file_time\"><input type=\"hidden\" name=\"fileLoc\" value=\"$lLink\"><input type=\"hidden\" name=\"status\" value=\"$dlState\"><input type=\"hidden\" name=\"story\" value=\"$dlName\"><input type=\"hidden\" name=\"viewtype\" value=\"ViewOnly\"><input type=\"submit\" value=\"View $dlName\"></form>";
			$progStatus = "<progress value=\"$steptovalue{$valStat}\"max =\"$maxValue\">Step $steptovalue{$valStat} of $maxValue</progress>";
			@startedCol = (@startedCol,"$progStatus|$valStat|$divHead|$col1Info|$actionButton");
	#	ClosedDIV("class","DL2of6Col","$progStatus <progress value=\"$steptovalue{$valStat}\"max =\"$maxValue\">Step $steptovalue{$valStat} of $maxValue</progress>");
		} else {
			$progStatus = "Posted!";
			$valStat = "Filtered";
			$CompleteTally++;
			$divHead = "DLHeadDone";
			$col1Info = "$dlName<hr>Last Modified: $file_time";
			$actionButton = "<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\"><input type=\"hidden\" name=\"tmp\" value=\"$tmp\"><input type=\"hidden\" name=\"modtime\" value=\"$file_time\"><input type=\"hidden\" name=\"fileLoc\" value=\"$lLink\"><input type=\"hidden\" name=\"status\" value=\"$dlState\"><input type=\"hidden\" name=\"story\" value=\"$dlName\"><input type=\"hidden\" name=\"viewtype\" value=\"ViewOnly\"><input type=\"submit\" value=\"View $dlName\"></form>";
			@completeCol = (@completeCol,"$progStatus|$valStat|$divHead|$col1Info|$actionButton");
		}
		#ClosedDIV("class","DL2of6Col","$col1Info");
		#ClosedDIV("class","DL2of6Col","$progStatus <progress value=\"$steptovalue{$valStat}\"max =\"$maxValue\">Step $steptovalue{$valStat} of $maxValue</progress>");
		#ClosedDIV("class","DL2of6Col","$actionButton");
		#EndDIV();
	}

} #END foreach $thisdl (@deadlinesThisWeek) 

if (($thisstate eq "Not Started") || ($thisstate eq "All")) {
	OpenDIV("class","DLHead","");
	ClosedDIV("class","DLHeadNS","Features Not Started Yet");
	if ($NotStartTally == 0) {
		ClosedDIV("class","DLHeadEmpty","All Features are started.");
	} else {
		foreach my $startedLine (@notStartedCol) {
			my @pipedLine = split('\|',$startedLine);
			#ClosedDIV("class","DLNSCard","$pipedLine[3]<br>$pipedLine[0]<br>$pipedLine[4]");
			ClosedDIV("class","DLNSCard","$pipedLine[3]<br>$pipedLine[4]");
		}
	} #END if ($StartTally > 0)
	EndDIV();
} # END if (($thisstate eq "Not Started") || ($thisstate eq "All"))

if (($thisstate eq "Started") || ($thisstate eq "All")) {
	OpenDIV("class","DLHead","");
	ClosedDIV("class","DLHeadST","Features Started");
	if ($StartTally == 0) {
		ClosedDIV("class","DLHeadEmpty","No Features in Progress.");
	} else {
		foreach my $startedLine (@startedCol) {
			my @pipedLine = split('\|',$startedLine);
			ClosedDIV("class","DLSTCard","$pipedLine[3]<br>$pipedLine[0]<br>$pipedLine[4]");
		}
	} #END if ($StartTally > 0)
EndDIV();
} # END if (($thisstate eq "Started") || ($thisstate eq "All"))

if (($thisstate eq "Complete") || ($thisstate eq "All")) {
	OpenDIV("class","DLHead","");
	ClosedDIV("class","DLHeadDone","Features Completed");
	if ($CompleteTally == 0) {
		ClosedDIV("class","DLHeadEmpty","No Features Completed yet.");
	} else {
		foreach my $startedLine (@completeCol) {
			my @pipedLine = split('\|',$startedLine);
			ClosedDIV("class","DLDoneCard","$pipedLine[3]<br>$pipedLine[0]<br>$pipedLine[4]");
		}
	} #END if ($CompleteTally > 0) 
	EndDIV();
}

EndDIV();
EndDIV();

#$StartTally
#$NotStartTally 
#$CompleteTally

EndDIV();
# Use $myweek to determine deadlines for up to 3 weeks away
my $percentComplete = ($CompleteTally / ($StartTally + $NotStartTally + $CompleteTally)) * 100;
$percentComplete = substr($percentComplete,0,4);
my $statWeek = uc($myweek);
my $statState = uc($thisstate);


EndDIV();
EndDIV();
HTMLend();


