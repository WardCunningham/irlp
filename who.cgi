#!/usr/bin/perl
use strict;

my ($node) = $ENV{QUERY_STRING} =~ /(\d+)/;
$node = '3042' unless $node;

print "Content-type: text/html\n\n";

my (%net, %nodes, $nets, %names);

open(S, "curl -s 'http://status.irlp.net/nohtmlstatus.txt.zip' | gunzip -c  | tee nodes.txt |") or die($!);
while (<S>) {
        my ($node, $call, $city, $state, $country, $status, $record, $install, $lat, $lon, $update, $freq, $offset, $pl, $owner, $url, $change) = split(/\t/);
        next unless $status =~ /^\d+$/;
        my $net = $net{$node} || $net{$status} || sprintf("%09d",++$nets);
        $net{$node} = $net{$status} = $net;
        $nodes{$net} .= "$node ";
        my $c = &ago($change);
        $url = "http://$url" unless !$url or $url =~ /^http:/;
        $call = "<a href=$url>$call</a>" if $url;
        $names{$node} = << ;
        <tr>
        <td><a href=http://status.irlp.net/IRLPnodedetail.php?nodeid=$node>$node</a></td>
        <td>$call</td>
        <td><a href=http://qrz.com/callsign/$owner>$owner</a></td>
        <td><a href=http://c2.com/~ward/irlp/rose.cgi?lat=$lat&lon=$lon>$city</a> $state $country</td>
        <td>$c</td>
        </tr>

}

my @nodes = split(/ /, $nodes{$net{$node}});
my $nodes = @nodes;

print <<, map($names{$_}, @nodes), << ;
<h1>Who's Called</h1>
<p>This table lists the $nodes nodes participating in node $node current call.
Reload the page for new information which may be up to one minute old.
An empty table means we aren't connected or haven't yet noticed the connection.
</p>
<table border cellspacing=0 cellpadding=5>
<tr>
        <td><b>Node</b></td>
        <td><b>Call</b></td>
        <td><b>Owner</b></td>
        <td><b>Location</b></td>
        <td><b>Change</b></td>

</table>

sub ago {
        my ($timestamp) = @_;
        days((time()-$timestamp)/24/60/60);
}

sub days {
        my $age = int($_[0] * 24 * 60 * 60);
        my $days = "$age seconds";
        $age = int($age / 60);  $days = "$age minutes" if $age >= 2;
        $age = int($age / 60);  $days = "$age hours" if $age >= 2;
        $age = int($age / 24);  $days = "$age days" if $age >= 2;
        $age = int($age / 7);   $days = "$age weeks" if $age >= 2;
        $age = int($age / 4);   $days = "$age months" if $age >= 2;
        $age = int($age / 12);  $days = "$age years" if $age >= 2;
        return $days;
}        

