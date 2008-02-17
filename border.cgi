#!/usr/bin/perl
use strict;
print "Content-Type: text/html\n\n";

my $image = $ENV{'QUERY_STRING'};
print <<;
<center>
<br><br><br>
<img src=$image>
<br><font color=gray>Copyright (c) 2003</font>
</center>


