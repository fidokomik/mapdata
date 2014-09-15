#!/usr/bin/perl
# Author: Petr Vileta, 2012
# License: WTFPL - Do What The Fuck You Want To Public License, http://sam.zoy.org/wtfpl/

use strict;
use DBI;
use CGI qw(:standard);
require 'init.pl';
$|=1;
our ($db,$dbhost,$dbport,$dbuser,$dbpw)=connect_db();
our $dbh = DBI->connect("DBI:mysql:$db:$dbhost:$dbport",$dbuser,$dbpw) or die "Can't connect: $DBI::errstr\n";
$dbh->do("SET character_set_client=utf8");
$dbh->do("SET character_set_connection=utf8");
$dbh->do("SET character_set_results=utf8");
my $forumgroup=get_setup('maingroup','number');
&xmlstart;
my $sth=$dbh->prepare("SELECT phpbb_users.user_id,username_clean,pf_fullname,user_from,user_website,user_avatar,user_avatar_width,user_avatar_height FROM phpbb_user_group
	LEFT JOIN phpbb_users ON (phpbb_users.user_id=phpbb_user_group.user_id)
	LEFT JOIN phpbb_profile_fields_data ON (phpbb_profile_fields_data.user_id=phpbb_user_group.user_id)
	WHERE phpbb_user_group.group_id=? AND pf_zobraz_na_mape=1");
$sth->execute($forumgroup) or die $sth->errstr;
my ($id,$name,$fullname,$from,$web,$avatar,$width,$height);
$sth->bind_columns(\($id,$name,$fullname,$from,$web,$avatar,$width,$height));
while ($sth->fetch)
	{
	$name=~s/\s+/\./;
	$avatar=~s/\s//g;
	$from=~s/\s+/ /sg;
	$from=~s/^\s+|\s+$//g;
	if($from)
		{
		if($avatar=~m/^\d/)
			{
			$avatar='https://forum.pirati.cz/download/file.php?avatar=' . $avatar;
			}
		print 	"\t<pirat>\n",
			"\t\t<id>$id</id>\n",
			"\t\t<jmeno>$fullname</jmeno>\n",
			"\t\t<mail>$name",'@pirati.cz',"</mail>\n",
			"\t\t<adresa>$from</adresa>\n",
			"\t\t<web>$web</web>\n",
			"\t\t<avatar>\n";
		if(length($avatar) > 0)
			{
			print	"\t\t\t<image>$avatar</image>\n",
				"\t\t\t<width>$width</width>\n",
				"\t\t\t<height>$width</height>\n";
			}
		print	"\t\t</avatar>\n",
			"\t</pirat>\n";
		}
	}
$sth->finish;
$dbh->disconnect;
print "</data>\n";


sub xmlstart
{
# html header
print <<"EOF";
Cache-Control: no-cache, no-store, no-transform, must-revalidate
Pragma: no-cache
Content-type: text/xml

<?xml version="1.0" encoding="utf-8"?>
<data>
EOF
} 
