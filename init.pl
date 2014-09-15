#!/usr/bin/perl
use strict;
1;
sub connect_db
{
#############################################
# nastavit dle potreby
#
my $db='???';
my $dbhost='localhost';
my $dbport='3308';
my $dbuser='???';
my $dbpw='???';
#############################################
return ($db,$dbhost,$dbport,$dbuser,$dbpw,0);
}
