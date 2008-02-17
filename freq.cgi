#!/usr/bin/perl

print "Content-type: text/plain\n\n";
open (N, "nodes.txt");
while (<N>) {
    next unless /USA|Canada/;
    next unless /\b0\.0000\b/; 
    $f{$1}++ if /\b(14[4-7]\.\d\d\d\d)\b/;
} 
for (sort keys %f) {
    print "$_ ", "x" x $f{$_}, "\n";
} 
