#fieldname|defaultvalue|inputtype|listofvalidvalues|Hint|require
name||text|||readonly
status|test|radio|test,live|Setting this live will put it into live production.
colnum|2|select|1,2,3|The number of newspaper columns to display in feature preview.|
dueday|Wednesday|select|Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday|Choose a deadline day.
duetime|1130|select|1130,1630|Select a due time.|
dueweek|2|select|1,2,3,4,5|Number of weeks out for Feature date.|
emailgroup|lrgonyea|textarea||Persons to email with Feature updates separated by commas. Please do not include @gracenote.|required
recycle|No|radio|Yes,No|Mark this feature as recyclable.
xmlFeature|No|radio|Yes,No|Mark this feature as an XMl Feature.
copy||text||Feature name that this feature can copy to. Field must include a feature name with no date.|optional
#photo||text||Add a photo name to include with this feature.|optional