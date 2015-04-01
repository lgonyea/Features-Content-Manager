#! /usr/bin/perl

use warnings;
use strict;
use Tie::File;
use File::Copy;
use CGI;
use File::Find;
require("FF_common_func.cgi");
my $homeIP = getHomeAddress();
my $mysearch;
my $SBinfo;
my @daysOfWeek = qw( Sunday Monday Tuesday Wednesday Thursday Friday Saturday );
my @shortdaysOfWeek = qw( Sun Mon Tue Wed Thu Fri Sat );

my @monthsOfYear = qw( January Febuary March April May June July August September October November December );
my @shortmonthsOfYear = qw( Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec );
my $mysearch = "";
my $step = "";
my $weekof = "";
my $writer = "";
my $homeDir = "/Library/WebServer/FF2/";
my $templateDir = "/Library/WebServer/CGI-Executables/templates/";

my $query = new CGI;

my $currenttime = GetDateTime();
print "Content-type: text/html\n\n";
print "<html>\n<head>\n";
print "<title>TMS Feature Writer Help Form</title>\n";
print "<meta charset=\"utf-8\">\n";
LoadCSS();
LoadJS();
print "</HEAD>\n\n";
print "<BODY bgcolor=\"lightgray\" color=\"whitesmoke\" link=\"black\" vlink=\"black\" text=\"black\">\n";
HeaderStart();
HeaderLeft("TMS Features Writer Help Form<br> <b>$currenttime</b>");
HeaderEnd();

#start the navigation bar
NavStart();

NavEnd();
ContainerStart();
ContentStart();
#print "<b>Features Writer Help Email Form</b><br>";
print "<h1>Please enter your email and give us a description of the problem or request.</h1><br><br>";
print "<h2>Larry Gonyea or Kyle Lewis will contact you as soon as possible.</h2><br><br>";
print "<form method=\"POST\" action=\"http://$homeIP/cgi-bin/FE2/emailer.cgi\">\n";
print "<input type=\"hidden\" name=\"TOline\" value=\"lrgonyea\@tribune.com,kdlewis\@tribune.com,bnelson\@tribune.com,jgalusha\@tribune.com\">";
my $SelectList = problemList();
print "<b>Choose a topic:</b><br>\n";
print "<select name=\"topic\">$SelectList</select><br><br>\n";
print "<b>Your email address:</b><br>\n";
print "<input type=\"text\" size=\"100\" name=\"FROMline\"><br><br>";
print "<b>Description of the problem:</b><br>\n";
print "<textarea rows=\"20\" cols=\"100\" class=\"ckeditor\" name=\"BODYline\">Help Question or Suggestion.</textarea><br>";
print "<input type=\"submit\" value=\"Submit Email\"><br>";
print "</form>\n";

ContentEnd();


ContainerEnd();
print "		</body>\n";
print "</html>\n";

sub problemList {
my @PList = ("General Question","Suggestion","Error on Site","New Feature Request");
my $optionslist = "";
		foreach my $choices (@PList) {
				$optionslist = ("$optionslist<option value=\"$choices\">$choices</option>\n");
		}	
return($optionslist);	
}

