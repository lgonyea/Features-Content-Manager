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
#my $baseFEfolder = "/Library/WebServer/CGI-Executables/FE";
#my $FeatFolder = "/Library/WebServer/FF2";
my ($baseFEfolder,$FeatFolder) = getFilesLocal();
my ($homeIP,$systemType) = getHomeAddress();
#my $homeIP = "localhost";
my $selfPage = "$homeIP/cgi-bin/FE2/featuremanager.cgi";
my $mysearch;
my $SBinfo;
my @feaInEdit = "";
my @daysOfWeek = qw( Sunday Monday Tuesday Wednesday Thursday Friday Saturday );
my @shortdaysOfWeek = qw( Sun Mon Tue Wed Thu Fri Sat );

my @monthsOfYear = qw( January Febuary March April May June July August September October November December );
my @shortmonthsOfYear = qw( Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec );
my $mysearch = "";
my $step = "";
my $weekof = "";
my $writer = "";
my $homeDir = "$FeatFolder/";
my $templateDir = "$baseFEfolder/templates/";
my ($week7,$week6,$week5,$week4,$week3,$week2,$week1,$weeknow) = getweeks(); 
my @allsteps = getstatelist();
my @allbaseweeks = getweeks();
my @deadlines = getFeatDeadlines();
my $query = new CGI;
my $pageType = $query->param('pageType');
my $mysearch = $query->param('search');
my $featsearch = $query->param('feature');
my $step = $query->param('step');
my $weekof = $query->param('weekof');
my $writer = $query->param('writer');

my $currenttime = GetDateTime();
makeHTML5type();
LoadCSS("featman2.css");
LoadJS();
JQfadeIn("#Content","slow");
JQtoggleComplete(".ContentCardComplete","compbutton");
JQtoggleNS(".ContentCardNS","nsbutton");
JQtoggleST(".ContentCard","stbutton");
JQtoggleNF(".SidebarHide","nfbutton");
print "</script>";

HTMLtitle("Gracenote Feature Writer");

OpenDIV("ID","Header");
makeHeaderTopper();

ClosedDIV("class","HeaderLeft","Gracenote Features Content Manager - $systemType System");
my $AllFeatList = getFileList("$baseFEfolder/templates/","No");
EndDIV();

#start the navigation bar
OpenDIV("ID","Nav");
## Create the drop down lists for filtering features.
OpenDIV("class","NavLeft",);
makeNAVbar();
EndDIV();

EndDIV();

###############


#############
#Begin building content area based on any filters applied
OpenDIV("ID","Container");


OpenDIV("ID","Sidebar");

ClosedDIV("class","SidebarTitle","Features in Edit","These features have been opened for editing and are locked. Resetting the feature will allow editing again.");

OpenDIV("class","SidebarGroup");
my @featInEdit = getFeatInEdit(); #makes a list of features that are in the TEMP folder indicating that the feature is being edited.
my $tmpcount = 0;
my @editingList = "";
foreach my $tmpfile (@featInEdit) { 
#	return format of getFeatInEdit: "storyname|step|path";
	if ($tmpfile ne "") {
		@editingList = (@editingList, $tmpfile);
		$tmpcount++;}
	}
ClosedDIV("class","SidebarStatHeader","Features being edited: $tmpcount");
if ($tmpcount > 0) {
	foreach (@editingList) {
		if ($_ ne "") {
				my @tmppart = split('\|',$_);
				
				print "<form method=\"get\" action=\"http://$homeIP/cgi-bin/FE2/FF_mover.cgi\">\n";
				print "<input type=\"hidden\" name=\"oldstate\" value=\"reset\">";
				print "<input type=\"hidden\" name=\"newstate\" value=\"reset\">";
				print "<input type=\"hidden\" name=\"fileLoc\" value=\"$tmppart[2]\">";
				print "<input type=\"hidden\" name=\"story\" value=\"$tmppart[0]\">";
				my $SideStat = "<b>$tmppart[0]</b> is open in <b>$tmppart[1]</b>.<br><input type=\"submit\" value=\"Click to Reset $tmppart[0]\">";
				#print "$SideStat";
				ClosedDIV("class","SidebarChoice",$SideStat,"$tmppart[0] is open for editing. Resetting this will feature will allow editing again, but changes will not be saved.");
				print "</form>";
		}
	}
}
EndDIV();

EndDIV();

OpenDIV("ID","Content");
if ($pageType eq "newFeat") {
ClosedDIV("class","ContentBoxPlain","Choose a feature in the drop down menus below to begin a new feature.<br> Note: if feature does not show in the drop down list here, then it has already been started for that week.");

my $showWeek = $week7;
my $weekfeatlist = getNewFeatslistoptions($showWeek);
	#		ClosedDIV("class","CardCatHead","Create a $week5 Feature");
	OpenDIV("class","ContentCardNSSH");
		ClosedDIV("class","ContentCardHead","Choose a $showWeek Feature");
	if ($weekfeatlist eq "No Features") {
			ClosedDIV("class","ContentCardBody","All Features started for $showWeek");
			ClosedDIV("class","ContentCardFooter","");
		} else {
			ClosedDIV("class","ContentCardBody","<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\"><select name=\"story\">$weekfeatlist</select><input type=\"hidden\" name=\"status\" value=\"new\">");
			ClosedDIV("class","ContentCardFooter","<input type=\"submit\" value=\"Create This Feature\"></form>\n");	
		}
	EndDIV();
	
my $showWeek = $week6;
my $weekfeatlist = getNewFeatslistoptions($showWeek);
	#		ClosedDIV("class","CardCatHead","Create a $week5 Feature");
	OpenDIV("class","ContentCardNSSH");
		ClosedDIV("class","ContentCardHead","Choose a $showWeek Feature");
	if ($weekfeatlist eq "No Features") {
			ClosedDIV("class","ContentCardBody","All Features started for $showWeek");
			ClosedDIV("class","ContentCardFooter","");
		} else {
			ClosedDIV("class","ContentCardBody","<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\"><select name=\"story\">$weekfeatlist</select><input type=\"hidden\" name=\"status\" value=\"new\">");
			ClosedDIV("class","ContentCardFooter","<input type=\"submit\" value=\"Create This Feature\"></form>\n");	
		}
	EndDIV();
	
my $showWeek = $week5;
my $weekfeatlist = getNewFeatslistoptions($showWeek);
	#		ClosedDIV("class","CardCatHead","Create a $week5 Feature");
	OpenDIV("class","ContentCardNSSH");
		ClosedDIV("class","ContentCardHead","Choose a $showWeek Feature");
	if ($weekfeatlist eq "No Features") {
			ClosedDIV("class","ContentCardBody","All Features started for $showWeek");
			ClosedDIV("class","ContentCardFooter","");
		} else {
			ClosedDIV("class","ContentCardBody","<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\"><select name=\"story\">$weekfeatlist</select><input type=\"hidden\" name=\"status\" value=\"new\">");
			ClosedDIV("class","ContentCardFooter","<input type=\"submit\" value=\"Create This Feature\"></form>\n");	
		}
	EndDIV();

my $showWeek = $week4;
my $weekfeatlist = getNewFeatslistoptions($showWeek);
	#		ClosedDIV("class","CardCatHead","Create a $week5 Feature");
	OpenDIV("class","ContentCardNSSH");
		ClosedDIV("class","ContentCardHead","Choose a $showWeek Feature");
	if ($weekfeatlist eq "No Features") {
			ClosedDIV("class","ContentCardBody","All Features started for $showWeek");
			ClosedDIV("class","ContentCardFooter","");
		} else {
			ClosedDIV("class","ContentCardBody","<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\"><select name=\"story\">$weekfeatlist</select><input type=\"hidden\" name=\"status\" value=\"new\">");
			ClosedDIV("class","ContentCardFooter","<input type=\"submit\" value=\"Create This Feature\"></form>\n");	
		}
	EndDIV();

my $showWeek = $week3;
my $weekfeatlist = getNewFeatslistoptions($showWeek);
	#		ClosedDIV("class","CardCatHead","Create a $week5 Feature");
	OpenDIV("class","ContentCardNSSH");
		ClosedDIV("class","ContentCardHead","Choose a $showWeek Feature");
	if ($weekfeatlist eq "No Features") {
			ClosedDIV("class","ContentCardBody","All Features started for $showWeek");
			ClosedDIV("class","ContentCardFooter","");
		} else {
			ClosedDIV("class","ContentCardBody","<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\"><select name=\"story\">$weekfeatlist</select><input type=\"hidden\" name=\"status\" value=\"new\">");
			ClosedDIV("class","ContentCardFooter","<input type=\"submit\" value=\"Create This Feature\"></form>\n");	
		}
	EndDIV();

my $showWeek = $week2;
my $weekfeatlist = getNewFeatslistoptions($showWeek);
	#		ClosedDIV("class","CardCatHead","Create a $week5 Feature");
	OpenDIV("class","ContentCardNSSH");
		ClosedDIV("class","ContentCardHead","Choose a $showWeek Feature");
	if ($weekfeatlist eq "No Features") {
			ClosedDIV("class","ContentCardBody","All Features started for $showWeek");
			ClosedDIV("class","ContentCardFooter","");
		} else {
			ClosedDIV("class","ContentCardBody","<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\"><select name=\"story\">$weekfeatlist</select><input type=\"hidden\" name=\"status\" value=\"new\">");
			ClosedDIV("class","ContentCardFooter","<input type=\"submit\" value=\"Create This Feature\"></form>\n");	
		}
	EndDIV();

my $showWeek = $week1;
my $weekfeatlist = getNewFeatslistoptions($showWeek);
	#		ClosedDIV("class","CardCatHead","Create a $week5 Feature");
	OpenDIV("class","ContentCardNSSH");
		ClosedDIV("class","ContentCardHead","Choose a $showWeek Feature");
	if ($weekfeatlist eq "No Features") {
			ClosedDIV("class","ContentCardBody","All Features started for $showWeek");
			ClosedDIV("class","ContentCardFooter","");
		} else {
			ClosedDIV("class","ContentCardBody","<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\"><select name=\"story\">$weekfeatlist</select><input type=\"hidden\" name=\"status\" value=\"new\">");
			ClosedDIV("class","ContentCardFooter","<input type=\"submit\" value=\"Create This Feature\"></form>\n");	
		}
	EndDIV();

#if ($week5featlist eq "No Features") {
#print "<b>All Available Features for $week5 have been started</b>";
#} else {
#print "<form method=\"post\" action=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi\"><select name=\"story\">$week5featlist</select><input type=\"hidden\" name=\"status\" value=\"new\"><input type=\"submit\" value=\"Create Feature\"></form>\n","Choose a feature to create for the week of $week5.";
#}
#EndDIV();

} elsif ($pageType eq "textSearch") {
#ClosedDIV("class","ContentBoxPlain","This function will search all text in all features for the weeks of $week5, $week4, $week3, $week2, $week1 and $weeknow. <br> Results will be displayed when search is completed.");
ClosedDIV("class","ContentBoxCenterPlain","Search for text in features for the weeks of $week7, $week6, $week5, $week4, $week3, $week2, $week1 and $weeknow.<br>");
ClosedDIV("class","ContentBoxCenterPlain","<form method=\"post\" name=\searchForm\" action=\"http://$homeIP/cgi-bin/FE2/featuremanager.cgi\"><input type=\"textarea\" rows=\"3\" name=\"search\" style=\"width:65%\" autofocus>\n");
ClosedDIV("class","ContentBoxCenterPlain","<input type=\"submit\" value=\"Search Feature Text\"></form>\n");
} elsif ($mysearch ne "") {
	#ClosedDIV("class","ContentInfo","Query results (Search: \"$mysearch\")");
#	OpenDIV("class","ContentForm");
#	EndDIV();
	showFeatmanoptions("search","$mysearch");
} 
elsif (($step ne "") && ($weekof ne "")) {
	#ClosedDIV("class","ContentInfo","Query results (Step = $step & Week of = $weekof)");
	showFeatmanoptions("stepweek","$step|$weekof");
} 
elsif ($step ne "") {
	#ClosedDIV("class","ContentInfo","Query results (Step = $step)");
	showFeatmanoptions("step","$step");
} 
elsif ($weekof ne "") {
							OpenDIV("class","ContentBoxPlain");
							#ClosedDIV("class","ContentCardHead","Show/Hide Not Started");
							#ClosedDIV("class","ContentCardBody","$col1Info");
#							ClosedDIV("class","FeatManButtons","<nsbutton>Show Not Started Features</nsbutton>");
							#EndDIV();
							#OpenDIV("class","ContentCardSH");
							#ClosedDIV("class","ContentCardHead","Show/Hide Started");
							#ClosedDIV("class","ContentCardBody","$col1Info");
							ClosedDIV("class","FeatManButtons","<stbutton>Hide Started Features</stbutton>");
							#EndDIV();
							#OpenDIV("class","ContentCardCompleteSH");
							#ClosedDIV("class","ContentCardHead","Show/Hide Completed");
							#ClosedDIV("class","ContentCardBody","$col1Info");
							ClosedDIV("class","FeatManButtons","<compbutton>Hide Completed Features</compbutton>");
							EndDIV();
							#ClosedDIV("class","ContentInfo","Query results (Week = $weekof)");
	showFeatmanoptions("weekof","$weekof");
} 
elsif ($writer ne "") {
	#ClosedDIV("class","ContentInfo","Query results (Writer = $writer)");
	showFeatmanoptions("writer","$writer");
} 
elsif ($featsearch ne "") {
	#ClosedDIV("class","ContentInfo","Query results (Feature = $featsearch)");
	showFeatmanoptions("feature","$featsearch");
} 
else {
	#ClosedDIV("class","ContentInfo","Showing all Features.");


							OpenDIV("class","ContentBoxPlain");
							#ClosedDIV("class","ContentCardHead","Show/Hide Not Started");
							#ClosedDIV("class","ContentCardBody","$col1Info");
							ClosedDIV("class","FeatManButtons","<nsbutton>Show Not Started Features</nsbutton>");
							#EndDIV();
							
							#OpenDIV("class","ContentCardSH");
							#ClosedDIV("class","ContentCardHead","Show/Hide Started");
							#ClosedDIV("class","ContentCardBody","$col1Info");
							ClosedDIV("class","FeatManButtons","<stbutton>Hide Started Features</stbutton>");
							#EndDIV();
							#OpenDIV("class","ContentCardCompleteSH");
							#ClosedDIV("class","ContentCardHead","Show/Hide Completed");
							#ClosedDIV("class","ContentCardBody","$col1Info");
							ClosedDIV("class","FeatManButtons","<compbutton>Hide Completed Features</compbutton>");
							EndDIV();


	showFeatmanoptions("all","all");
}


EndDIV();
EndDIV();
HTMLend();


