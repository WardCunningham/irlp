#!/usr/bin/perl
use strict;

print "content-type: text/html\n\n";


my $nodes = "nodes.txt";
my $detail = "http://status.irlp.net/?nodeid";
my $dx = $1 if $ENV{QUERY_STRING} =~ /(dx)/;
my $maxweeks = $dx ? 24 : 12;
if (!-e $nodes or -z $nodes or -M $nodes > (1/24/60)) {
    open (N, "curl -s 'http://status.irlp.net/nohtmlstatus.txt.zip' | gunzip -c  | tee $nodes |") or die($!);
} else {
    open (N, $nodes) or die($!);
}

my (%repeater, %simplex);
<N>;
while (<N>) {
    my ($node, $call, $city, $state, $country, $status, $record, $install,
        $lat, $lon, $update, $freq, $offset, $pl, $owner, $url, $change) = split /\t/;
    next unless $status eq 'IDLE';
    next unless $city;
    next if $dx and ($country eq 'USA' or $country eq 'Canada');

    my ($y, $m, $d) = split /-/, $install;
    my $days = int( ($^T/24/60/60) - (365.25*($y-1970)+30.5*($m-1)+$d) );
    my $hour = (24 + int($^T/60/60 % 24) + int($lon*24/360)) % 24;
    $hour = $hour<=12 ? $hour . " am" : ($hour - 12) . " pm";
    $hour =~ s/^0 /12 /;
    $hour = $lon ? "<font color=gray>$hour</font>" : "";
    my $weeks = int($days/7);
    next if $weeks > $maxweeks;

    ($city, $hour) = ("TBD", "") if /Information not yet provided/i;
    $url = "http://$url" if $url and not ($url =~ /^http:/);
    my $site = "<a href=$url>o</a>" if $url;
    my $rose = $lat && $lon ? "<a href=http://c2.com/~ward/irlp/rose.cgi?lat=$lat&lon=$lon>$state $country</a>" : "<font color=gray>$state $country</font>";
    my $description = "<a href=$detail=$node>$city</a> $rose  $hour $site <br>";
    if ($offset == 0) {
        $simplex{$weeks} .= $description;
    } else {
        $repeater{$weeks} .= $description;
    }
}

print <<;
    <center>
    <h1>Newest IRLP Nodes</h1>
    These newly installed $dx nodes are currently online and idle.
    <br>
    <table border=0 cellpadding=8 cellspacing=0>
    <tr>
    <td valign=top>weeks
    <td valign=top>repeater
    <td valign=top>simplex

for (0..$maxweeks) {
    my $color = ($_%2) ? "#88FF88" : "#AAFFAA";
    print <<;
        <tr bgcolor=$color>
        <td valign=top align=center>$_
        <td valign=top>$repeater{$_}
        <td valign=top>$simplex{$_}

}
print <<;
    </table>
    <p>
    <font color=gray>
        About Newest Nodes
    </font>
    <table width=400><tr><td>
        <font size=-1 color=gray>
        This program selects from
        <a href=//www.irlp.net>$. IRLP nodes</a>
        choosing those with an installation date within the last $maxweeks weeks.
        Only nodes that are ready to accept connections are shown. 
        We presume new node owners and users would love to get a call from you.
        Select the node location to learn more about the node.
        The time listed after most nodes is a guess at the local time at the site.
        The occasional trailing o is a link to the node's web site, if any.  
        Try this <a href=newest.cgi?dx>dx version</a>
        which looks for the newest nodes outside the US and Canada. 
        </font>
        </td></tr>
    </table>
    <p><font size=-1><a href=/~ward>Ward Cunningham k9ox</a></font>
    </body></html>

