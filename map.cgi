#!/usr/bin/perl

print <<"EOF";
Content-type: text/html

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml">
  <head>
    <script src="http://maps.google.com/maps?file=api&v=1&key=ABQIAAAAtBAZBAMoB0ro31zfcfL_TBRiLeasGpXa3BkOW7yBZqA6KP7-qxQnEtngH58z_k8W90yRjfQ-lWk2ew" type="text/javascript"></script>
    <style type="text/css">
    v\:* {
      behavior:url(#default#VML);
    }
    </style>
  </head>
  <body>
EOF

my ($mylat, $mylon) = (45.47009, -122.74593);
$mylat = $1+0 if $ENV{QUERY_STRING} =~ /lat=(-?\d*(\.\d+)?)/;
$mylon = $1+0 if $ENV{QUERY_STRING} =~ /lon=(-?\d*(\.\d+)?)/;

my $nodes = "nodes.txt";
my $url = "http://status.irlp.net/nohtmlstatus.txt";

if (!-e $nodes or -z $nodes or -M $nodes > 1) {
    open (N, "TMPDIR=/tmp TERM=vt100d lynx -source $url | tee $nodes |") or die($!);
} else {
    open (N, $nodes) or die($!);
}

my $script = <<;
// generated calls
var point;

while (<N>) {
    my ($node, $call, $city, $state, $country, $status, $record, $install,
        $lat, $lon, $update, $freq, $offset, $pl, $owner, $url, $change) = split /\t/;
    ($lat, $lon) = ($lat+0, $lon+0); # avoid leading 0 which messes up javascript
    my ($dx, $dy) = (($lon-$mylon)/2, $lat-$mylat);
    my $dist = sprintf("%06d", 100*(abs($dx)+abs($dy)));
    next unless $dist < 300;
    next if $dist < 0; # bad data in db
    my $idist = $dist+0;
    my $web = "<a href=$url>o</a>" if $url;
    $freq =~ s/0.0000/000.0000/;
    $freq = "<b>$freq</b>" if $offset != 0;
    my $item = "$owner&nbsp;$status&nbsp;<a href=http://status.irlp.net/IRLPnodedetail.php?nodeid=$node>$freq</a> <a href=rose.cgi?${map}lat=$lat&lon=$lon>$city $state</a> <font color=gray>($idist)</font> $web <br>";
    $item =~ s/"/''/g;
    $script .= " point = new GPoint($lon, $lat);\n map.addOverlay(createMarker(point, \"$item\"));\n"

}

print <<"EOF";
<div id="map" style="width: 100%; height: 600px"></div>
    <script type="text/javascript">
    //<![CDATA[
    
    var map = new GMap(document.getElementById("map"));
    map.addControl(new GLargeMapControl());
    map.addControl(new GMapTypeControl());
    map.centerAndZoom(new GPoint($mylon, $mylat), 8);
    //map.zoomTo(7);

// Create a marker whose info window displays the given number.
function createMarker(point, html) {
  var marker = new GMarker(point);

  // Show this marker's index in the info window when it is clicked.
  GEvent.addListener(marker, 'click', function() {
    marker.openInfoWindowHtml(html);
  });

  return marker;
}

var point;
$script


    //]]>
    </script>
  </body>
</html>
EOF

