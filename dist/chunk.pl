#!/usr/bin/perl
use strict;
use Time::HiRes qw( gettimeofday tv_interval );

my $history;
my ($t0, $t1);
$t0 = [gettimeofday];

open (R, "bin/readinput|");
while (<R>) {

	$t1 = [gettimeofday];
	my $elapsed = tv_interval ( $t0, $t1);
        $t0 = $t1;

	$history .= " " if $elapsed > 1;
	$history .= " " if $elapsed > 10;
	$history .= "{" if /COS ACTIVE/;
	$history .= "}" if /COS INACTIVE/;
	$history .= "(" if /PTT ACTIVE/;
	$history .= ")" if /PTT INACTIVE/;
	$history .= "<" if /FORCE KEY BIT SET/;
	$history .= ">" if /FORCE KEY BIT RESET/;
	$history .= $1  if /DTMF (.)/;

	$history =~ s/.*(.{20})/$1/;
#	print "$elapsed $history $_";
	$_ = $history;

	&connect("9200") if / {}{}{ }$/;
	&connect("9990") if / {}{}{}{ }$/;
}


sub connect {
	my ($node) = @_;
	my $dtmf = -e "local/active" ? "73" : $node;
#	print "decode $dtmf\n";
	my $result = `scripts/decode $dtmf`;
#	print $result;
}
