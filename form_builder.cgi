#! /usr/bin/perl
##########################################
#
#	by Larry Gonyea
#      TMS
#  The Feature_Editor script creates new features as well as opens existing features.
#  It takes information from the template file to determine the field type and field name
#  If this is opening a feature already started, it will display information from the feature within the fieldname tags and place it in the correct form fields.
#  
###############################################

sub MakeAForm {
# p0 = path to form Form Template to get from. this file will dictate every form line type, default value, input type etc.
# p1 = Existing file to input from that you wish to update with the form. (Use "new" here to create a new file)
# p2 = Form ID (optional)
# p3 = Form title (optional)
# p4 = Name of new file if p1 is new.
my @params = @_;
	my $formTemplate = $_[0];
	my @specTempArray = arrayFile("$formTemplate");
	my $formFile = $_[1];
	my %FileHash = hashAFile("$formFile");
	my $formID = $_[2];
	my $formTitle = $_[3];
	my $newFile = $_[4];
	#print "formFile is $formFile<br>";
	#print "My template is $formTemplate<br>";
	#print "This form will be called $newFile<br>";
	
	if ($formTitle ne '') {
		ClosedDIV("Class","formTitle","$formTitle");
	}
	foreach (@specTempArray) {
		my $option;
		my $optionsList;
		if ($_ =~ m/^#/) { #Line that starts with # symbol is informational about the columns
			next;
		} else {
			my @lineParts = split('\|',$_);
			my $fieldName = $lineParts[0];
			$fieldName =~ s/^\s+|\s+$//g;

			my $defValue = $lineParts[1];
			$defValue =~ s/^\s+|\s+$//g;
				
			my $inputType = $lineParts[2];
			$inputType =~ s/^\s+|\s+$//g;
				if (($inputType eq "select") || ($inputType eq "radio")) {
					my $listValues = $lineParts[3];
					$listValues =~ s/^\s+|\s+$//g;
					#print "Value list for $fieldName is $listValues\n";
					my @listofValues = split(',',$listValues);
					#if ($formFile eq "new") {
					#	my $selectedValue = $defValue;
					#} else {
						my $selectedValue = $FileHash{$fieldName};
					#}
					foreach $thisOption (@listofValues) {
						#print "option is $thisOption<br>\n";
						if ($thisOption eq $selectedValue) {
							#print "Found a match with $thisOption and $selectedValue<br>\n";
							if ($inputType eq "select") {
								$optionsList = "$optionsList<option value=\"$thisOption\" selected>$thisOption</option>\n";
							} else { #must be radio buttons
								$optionsList = "$optionsList<input type=\"radio\" name=\"$fieldName\" value=\"$thisOption\" checked>$thisOption";
							}
						} else {
							if ($inputType eq "select") {
								$optionsList = "$optionsList<option value=\"$thisOption\">$thisOption</option>\n";
							} else { #must be radio buttons
								$optionsList = "$optionsList<input type=\"radio\" name=\"$fieldName\" value=\"$thisOption\">$thisOption";
							} #if ($inputType eq "select")
						} #if ($thisOption eq $selectedValue) 
					} #foreach $thisOption (@listofValues) 
				} #if (($inputType eq "select") || ($inputType eq "radio")) 
			my $inputHint = $lineParts[4];
			my $inputReq = $lineParts[5];
			$inputHint =~ s/^\s+|\s+$//g;
			my $labelVal = uc($fieldName);
			### This breaks the whole thing. Grrr!!!
			#print "$inputType - $OptionsList<br>";
			#if ($formFile eq "new") {
			#	if ($labelVAL eq "NAME") {
			#		my $fieldValue = $newFile;
			#	} else {
			#		my $fieldValue = $defValue;
			#	}
			#} else {
				my $fieldValue = $FileHash{$fieldName};
			#}
		#	print "Value for $fieldName is $fieldValue type is $inputType<br>\n";			
			if ($inputType eq "text")  { 
				ClosedDIV("class","formLine","<label>$labelVal<div class=\"fieldHint\">${inputHint}</div></label>");
			#	if ((($inputReq eq "readonly") && ($formFile ne "new")) || ($labelVAL eq "NAME")) {
				if ($inputReq eq "readonly")  {
					ClosedDIV("class","formLine","<input type=\"text\" cols=\"100\" name=\"$fieldName\" value=\"$fieldValue\" readonly>");
				} else { 
					ClosedDIV("class","formLine","<input type=\"text\" cols=\"100\" name=\"$fieldName\" value=\"$fieldValue\">");
				}			
			} elsif ($inputType eq "textarea") { #make a drop down menu
				ClosedDIV("class","formLine","<label>$labelVal</label><div class=\"fieldHint\">${inputHint}</div>");
				ClosedDIV("class","formLine","<textarea rows=\"2\" cols=\"100\" name=\"$fieldName\" value=\"$fieldValue\">$fieldValue</textarea>");
			} elsif ($inputType eq "select") { #make a drop down menu
				ClosedDIV("class","formLine","<label>$labelVal</label><div class=\"fieldHint\">${inputHint}</div>");
				ClosedDIV("class","formLine","<select name=\"$fieldName\">$optionsList</select>");
			} else { #radio buttons are all that's left
				ClosedDIV("class","formLine","<label>$labelVal</label><div class=\"fieldHint\">${inputHint}</div>");
				ClosedDIV("class","formLine","$optionsList");
			} #if ($inputType eq "text") 
		} #if ($_ =~ m/^#/)
	} #foreach (@specTempArray)
} #sub MakeAForm

sub StartAForm {
# p1 Form ID (optional)
# p2 Form action aka cgi page (required) 
# p3 Hidden fields needed. Needs to come in as Name>Value|Name>Value|etc for each name value pair
}

sub ProcessAForm {

}

sub EndAForm {

}
1;