#!/usr/bin/perl

if ($#ARGV == -1) {
	print "Include file size as 2^n\n";
	exit;
}

if ($ARGV[0] > 32) {
	print "Cannot do exponent higher than 32..";
	exit;
}

`touch tempfile.swap`;
`touch hugefile.big`;
#`echo "abcdefgh" > hugefile.big`;
`echo "a" > hugefile.big`;


for ($i=1;$i<$ARGV[0];$i++) {
	`cat hugefile.big > tempfile.swap`;
	`cat tempfile.swap >> hugefile.big`;
}

`rm tempfile.swap`;


