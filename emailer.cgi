#! /usr/bin/perl

use warnings;
use strict;
use Tie::File;
use File::Copy;
use CGI;
use File::Find;
use lib "/opt/local/lib/perl5/site_perl/5.8.9";
use MIME::Lite;

require("FF_common_func.cgi");

my $query = new CGI;
my $emlTo = $query->param('TOline');
my $emlFrom = $query->param('FROMline');
my $emlBody = $query->param('BODYline');
my $emlTopic = $query->param('topic');
my @ticksplit = split('@',$emlFrom);
my $tickname = $ticksplit[0];
my $time = time();
my $tickfile = "/Library/WebServer/CGI-Executables/HELP/${tickname}_${time}.tik";
my $currenttime = GetDateTime();
#Check to see if we want to recycle this feature for later

	print "Content-type: text/html\n\n";
	print "<html>\n<head>\n";
	print "<title>Thank You</title>\n";
	print "<meta charset=\"utf-8\">\n";
	print "</head>\n";
	print "<body bgcolor=\"lightgray\">\n";
	
LoadEditorCSS();
LoadJS();
HeaderStart();
HeaderLeft("<b>Thank You.<br>Your email has been sent.</b>");
#HeaderRight("HELP");
HeaderEnd();
ContainerStart();
ContentStart();
if (!defined($emlTo) || $emlTo eq "") {
my $emlTo = "lrgonyea\@tribune.com";
}
if (!defined($emlFrom) || $emlFrom eq "") {
my $emlFrom = "FeatureWriterHelper\@tribune.com";
}
if (!defined($emlBody) || $emlBody eq "") {
my $emlBody = "Hey there was no body defined";
}
my $emlSubject = "Features Writer request from $emlFrom";

open Htick,">",$tickfile;
print Htick "ticket from: $tickname\n";
print Htick "Time: $currenttime\n";
print Htick "Topic: $emlTopic\n";
print Htick "Ticket: $emlBody\n\n";
print Htick "Ticket sent to $emlTo\n";
print Htick "Ticket sent from $emlFrom\n";
close Htick;

    my $msg = MIME::Lite->new(
    From => "lrgonyea",
    To   => "$emlTo",
    Cc   => "lrgonyea\@tribune.com",
    Subject => "$emlSubject",
    Type => "text/html",
    Data => "<body>$emlBody</body>",
    
    );
	$msg->send();

    
print "<h1>Your email has been sent and you should receive a copy of your request shortly</h1> <br> ";
print  "From: $emlFrom<hr><br> $emlBody <br> <br> ";
print "<b>We will respond as soon as possible.<br>\n";
print "<b>You can now close this window.<br>\n";

print "Thank You<br></b>";


ContentEnd();

ContainerEnd();
#print "</body></html>";

#need to return to featman.cgi or home page
print "		</body>\n";
print "</html>\n";