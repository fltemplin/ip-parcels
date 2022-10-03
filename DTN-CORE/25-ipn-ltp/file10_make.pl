#!/usr/bin/perl

if ($#ARGV == -1) {
	print "Include file size as 10^n\n";
	exit;
}

if ($ARGV[0] > 10) {
	print "Cannot do exponent higher than 10..";
	exit;
}

`touch tempfile.swap`;
`touch hugefile.big`;
#`echo "abcdefgh" > hugefile.big`;
`echo "abcdefghi" > hugefile.big`;


for ($i=1;$i<$ARGV[0];$i++) {
	`cat hugefile.big > tempfile.swap`;
	for ($j=1;$j<10;$j++) {
	`cat tempfile.swap >> hugefile.big`;
	}
}

`rm tempfile.swap`;


