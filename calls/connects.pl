#!/usr/bin/perl
use strict;
my (%net, %nodes, $nets);

while (<>) {
        my ($node, $call, $city, $state, $country, $status, $record, $install, $lat, $lon, $update, $freq, $offset, $pl, $owner, $url, $change) = split(/\t/);
        next unless $status =~ /^\d+$/;
        my $net = $net{$node} || $net{$status} || sprintf("%09d",++$nets);
        $net{$node} = $net{$status} = $net;
        $nodes{$net} .= "$node ";
}

for (sort keys %nodes) {
        my $nodes = $nodes{$_};
        my @nodes = split(/ /, $nodes);
        next unless $#nodes;
        print $nodes, "\n";
}
