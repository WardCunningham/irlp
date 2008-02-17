#!/usr/bin/perl
use strict;
print "Content-type: text/plain\n\n";

my %node;
my %mark;

sub abs {
        my ($v) = @_;
        return $v>=0 ? $v : -$v;
}

open (F, "nodes.txt");
while (<F>) {
        my ($node, $call, $city, $state, $country, $status, $record, $install, $lat, $lon, $update, $freq, $offset, $pl, $owner, $url, $change) = split(/\t/);
        next unless $city =~ /\w/;
        $city =~ s/ /_/g;
        $city =~ s/\W//g;
        $city =~ s/__+/_/g;
        next unless $lat and abs($lat) <= 90;
        next unless $lon and abs($lon) <=180;
        $node{$node} = "$node $city $lat $lon";
}

for my $file (split(/\n/, `ls -tr recent`)) {
        open (F, "recent/$file");
        print "time $file\n";
        while (<F>) {
                for my $num (split(/ /)) {
                        next unless $num =~ /\d+/;
                        $node{$num} = "$num Unknown_Node " . (35+rand(10)) . " " . (-35+rand(10)) unless $node{$num};
                        print "node $node{$num}\n" unless $mark{$num}++;
                }
                print "call $_";
        }
        print "\n";
}
