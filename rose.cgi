#!/usr/bin/perl
use strict;

print "content-type: text/html\n\n";

my ($mylat, $mylon) = (45.47009, -122.74593);
$mylat = $1 if $ENV{QUERY_STRING} =~ /lat=(-?\d*(\.\d+)?)/;
$mylon = $1 if $ENV{QUERY_STRING} =~ /lon=(-?\d*(\.\d+)?)/;
my $map = "$1&" if $ENV{QUERY_STRING} =~ /(map)/;

my $table;
my $directions = ['n','ne','e','se','s','sw','w','nw'];
my $nodes = "nodes.txt";
my $url = "http://status.irlp.net/nohtmlstatus.txt";

if (!-e $nodes or -z $nodes or -M $nodes > 1) {
    open (N, "curl -s 'http://status.irlp.net/nohtmlstatus.txt.zip' | gunzip -c  | tee $nodes |") or die($!);
} else {
    open (N, $nodes) or die($!);
}

while (<N>) {
    my ($node, $call, $city, $state, $country, $status, $record, $install,
        $lat, $lon, $update, $freq, $offset, $pl, $owner, $url, $change) = split /\t/;
    my ($dx, $dy) = (($lon-$mylon)/2, $lat-$mylat);
    my $dist = sprintf("%06d", 100*(abs($dx)+abs($dy)));
    next if $dist < 0; # bad data in db
    my $idist = $dist+0;
    next if $dist > 1000;
    my $web = "<a href=$url>o</a>" if $url;
#    my $stat = 
#        ($status eq 'DOWN' or $status eq 'OFFLINE') ? "<font color=red>x</font>" :
#        $status =~ /^9/ ? "<font color=gray>r</font>" :
#        $status =~ /^\d+/ ? "<a href=http://status.irlp.net/?nodeid=$status>n</a>" :
#        "<font color=gray>-</font>" ;
    $freq =~ s/0.0000/000.0000/;
    $freq = "<b>$freq</b>" if $offset != 0;
    my $item = <<;
        <a href=http://status.irlp.net/?nodeid=$node>$freq</a>
        <a href=rose.cgi?${map}lat=$lat&lon=$lon>$city $state</a>
        <font color=gray>($idist)</font> $web <br>

    my $bering = atan2($dx,$dy)/3.14159*180;
    my $dir = $directions->[int(($bering+360+22.5)/45)%8];
    $dir = 'c' if $dist < 20;
    $table->{$dir}{$dist} .= $item;
}

for my $cell (@$directions, 'c') {
    my %items = %{$table->{$cell} || {}};
    my @keys = (sort keys %items)[0..5];
    @keys = reverse @keys if $cell =~ /^n/;
    $table->{$cell} = join('', map $items{$_}, @keys) || "&nbsp; " x 20;
}

my $url = "http://www.vicinity.com/gif?&CT=$mylat:$mylon:1000000&W=340&H=240&FAM=myblast";
my $bg = "width=320 height=240 background=$url" if $map;
my $notmap = "map&" unless $map;
my $with = $notmap ? "with a" : "without the" ;

print << ;
    <html><head>
        <title>IRLP Compass Rose</title>
        <META NAME="ROBOTS" CONTENT="NOINDEX, NOFOLLOW">
        </head><body>
    <style>
        a         {text-decoration: none;}
        a:link    {color: #d64;}
        a:visited {color: #864;}
        a:hover   {text-decoration: underline}
        a:active  {text-decoration: underline}
    </style>
    <center>
    <h1>IRLP<img src=rose.jpg valign=center>Compass Rose</h1>
    <table cellpadding=10 border=1 cellspacing=0>
        <tr>
            <td valign=bottom>$table->{nw}</td>
            <td valign=bottom>$table->{n}</td>
            <td valign=bottom>$table->{ne}</td>
        </tr>
        <tr>
            <td valign=center>$table->{w}</td>
            <td valign=center $bg>$table->{c}
                <center><a href=map.cgi?lat=$mylat&lon=$mylon>map</a></center></td>
            <td valign=center>$table->{e}</td>
        </tr>
        <tr>
            <td valign=top>$table->{sw}</td>
            <td valign=top>$table->{s}</td>
            <td valign=top>$table->{se}</td>
        </tr>
    </table>
    <br>
    <table border=0 cellpadding=10>
        <tr>
            <td align=center>
                <a href=rose.cgi?${map}lat=35.6&lon=139.67>Tokyo</a><br>
                <a href=rose.cgi?${map}lat=13.11&lon=80.11>Madras</a><br>
            <td align=center>
                <a href=rose.cgi?${map}lat=61.15002&lon=-149.824>Anchorage</a><br>
                <a href=rose.cgi?${map}lat=21.305628&lon=-157.81803>Honolulu</a><br>
            </td><td align=center>
                <a href=rose.cgi?${map}lat=47.52658&lon=-122.35401>Seattle</a><br>
                <a href=rose.cgi?${map}lat=33.994047&lon=-118.2>Los Angeles</a><br>
            </td><td align=center>
                <a href=rose.cgi?${map}lat=39.715&lon=-104.98>Denver</a><br>
                <a href=rose.cgi?${map}lat=39.76001&lon=-86.17016>Indianapolis</a><br>
            </td><td align=center>
                <a href=rose.cgi?${map}lat=40.75&lon=-73.95>New York</a><br>
                <a href=rose.cgi?${map}lat=35.789211&lon=-78.71992>Raleigh</a><br>
            </td><td align=center>
                <a href=rose.cgi?${map}lat=51.5063&lon=0.1271>London</a><br>
                <a href=rose.cgi?${map}lat=-33.8&lon=151.2>Sydney</a><br>
            </td>
        </tr>
    </table>
    <p>
    <font color=gray>
        About Compass Rose
    </font>
    <table width=400><tr><td>
        <font size=-1 color=gray>
        The Compass Rose selects from
        <a href=//www.irlp.net>$. IRLP nodes</a>
        choosing those in the vicinity of a specified position.
        The closest nodes appear in the center square.
        The surrounding eight squares list more distant nodes in the direction of each compass point.
        Select a node or city to make it the center of the rose.
        Select a node operating frequency (bold for repeaters) to learn more about the node.
        The parenthesised numbers are distance approximations.
        The occasional trailing o is a link to the node's web site, if any.  
        </font>
        </td></tr>
    </table>
    <p><font size=-1><a href=/~ward>&copy;2003 Ward Cunningham k9ox</a></font>
    </body></html>

my $disabledFeature = <<;
    Try <a href=rose.cgi?${notmap}lat=$mylat&lon=$mylon>this version</a>
    $with map background for the center square. 


