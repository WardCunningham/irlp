#!/usr/bin/perl
use strict;
my (%net, %nodes, $nets);

while (<>) {
        my ($node, $call, $city, $state, $country, $status, $record, $install, $lat, $lon, $update, $freq, $offset, $pl, $owner, $url, $change) = split(/\t/);
        print "$node $status\t$city $country\n";
}

