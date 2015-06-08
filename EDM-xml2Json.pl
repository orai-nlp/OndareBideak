use strict;
use warnings;
#use XML::XML2JSON;
use XML::Simple;
use Data::Dumper;

use XML::XPath;
use XML::XPath::XMLParser;

use HTML::Entities;



#iconv -f ISO-8859-15 -t UTF-8 paths_zerrenda_20150423_Json.json > paths_zerrenda_20150423_Json_UTF8.json


my $dir=$ARGV[0];
my $OS_ERROR; 

print "[";   #HASI  ITEM ZERRENDA
print "\n";
my $pk=1;
foreach my $fp (glob("$dir/*.xml")) {
   # printf "%s\n", $fp;
    
    print "{";   #HASI  ITEMA
    print "\n";
    print "\"model\":\"kulturbideak_app.item\",";
    print "\n";
    print "\"pk\":$pk,";
    print "\n";
    print "\"fields\": {";  #HASI  FIELDS
    print "\n";
    
    
    my $xp = XML::XPath->new(filename => $fp);
    
    
#uri
    my $path_uri="/OAI-PMH/GetRecord/record/metadata/rdf\:RDF/ore\:Aggregation/edm\:aggregatedCHO"; 
    my $nodeset = $xp->find($path_uri);
    print "\"uri\":"."\"";
    foreach my $node ($nodeset->get_nodelist) {
	
	#print XML::XPath::XMLParser::as_string($node), "\n";
	#print $node->string_value;
	
	my $attribute="rdf:resource";
	print $node->getAttribute($attribute);
	
    }
    print "\","."\n";
    
#usfd_id ??? eremu hau hemen sartu behar da
    
# dc: Eremuen balioak lortu
    
    my $path_zati="/OAI-PMH/GetRecord/record/metadata/rdf\:RDF/edm\:ProvidedCHO/";
    my $dc_eremuak="title,creator,subject,description,publisher,contributor,date,type,format,identifier,source,language,relation,rights,coverage";
    my @dceremuak=split(',',$dc_eremuak);

    foreach my $eremu_izena (@dceremuak)
    {
	my $path_dc=$path_zati."dc\:$eremu_izena";
	$nodeset = $xp->find($path_dc);
	print "\"dc_$eremu_izena\":"."\"";
	foreach my $node ($nodeset->get_nodelist) 
	{   
	    my $str=$node->string_value; 
	    $str =~ s/^\s+|\s+$/ /g;
	    $str =~ s/\n//g;
	    $str=decode_entities($str);#html entitateak tratatu
	    $str=~ s|<.+?>||g; #html etiketak kendu
	    $str=~ s|"|'|g; #html etiketak kendu
	    print $str."  "; # bat baino gehiago dagoenerako
	    #print $node->string_value;         
	}
	print "\","."\n";

    }
    
# dcterms: Eremuen balioak lortu

    my $dcterms_eremuak="provenance,ispartof,temporal,spatial,medium,extent,alternative,issued,tableofcontents,isreplacedby";
    my @dctermseremuak=split(',',$dcterms_eremuak);

    foreach my $eremu_izena (@dctermseremuak) 
    {
	my $path_dcterms=$path_zati."dcterms\:$eremu_izena";
	$nodeset = $xp->find($path_dcterms);
	print "\"dcterms_$eremu_izena\":"."\"";
	foreach my $node ($nodeset->get_nodelist) 
	{   
	    my $str=$node->string_value; 
	    $str =~ s/^\s+|\s+$/ /g;
	    $str =~ s/\n//g;
	    print $str." "; # bat baino gehiago dagoenerako
	   # print $node->string_value;         
	}
	print "\","."\n";
    }
#edm: Eremuen balioak lortu (datu-basean europeana_ izenarekin hasten diren balioak)
    # unstored,country,language,uri,usertag,year,previewNoDistribute,hasobject      HAUEK NON??? ????????????

    my $path_zati_agg="/OAI-PMH/GetRecord/record/metadata/rdf\:RDF/ore\:Aggregation/";
    my $edm_eremuak_aggregation="object,provider,dataProvider,rights,isShownAt,isShownBy,unstored,country,language,uri,usertag,year,previewNoDistribute,hasobject";
    my @edmeremuak_aggregation=split(',',$edm_eremuak_aggregation);
   
    foreach my $eremu_izena (@edmeremuak_aggregation) 
    {

	if($eremu_izena eq "object" || $eremu_izena eq "rights" || $eremu_izena eq "isShownAt" ||  $eremu_izena eq "isShownBy")
	{
	    my $eremu_izena_lc=lc($eremu_izena);
	    my $atr="rdf:resource";
	    my $path_edm=$path_zati_agg."edm\:$eremu_izena";
	    $nodeset = $xp->find($path_edm);
	    print "\"edm_$eremu_izena_lc\":"."\"";
	    foreach my $node ($nodeset->get_nodelist) 
	    {   
		#my $attribute="rdf:resource";
		#print $node->getAttribute($attribute);
	   	my $str = $node->getAttribute($atr);
	#	print $node->string_value;    
		print $str;
	    }
	}
	else
	{
	    my $eremu_izena_lc=lc($eremu_izena);
	    my $path_edm=$path_zati_agg."edm\:$eremu_izena";
	    $nodeset = $xp->find($path_edm);
	    print "\"edm_$eremu_izena_lc\":"."\"";
	    foreach my $node ($nodeset->get_nodelist) 
	    {   
		my $str=$node->string_value; 
		$str =~ s/^\s+|\s+$/ /g;
		$str =~ s/\n//g;
		print $str." "; # bat baino gehiago dagoenerako
		# print $node->string_value;         
	    }
	}

	print "\","."\n";
	
    }

    my $path_zati_provcho="/OAI-PMH/GetRecord/record/metadata/rdf\:RDF/edm\:ProvidedCHO/";
    my $edm_eremuak_providedCHO="type";
    my @edmeremuak_providedCHO=split(',',$edm_eremuak_providedCHO);

    foreach my $eremu_izena (@edmeremuak_providedCHO) 
    {
	my $eremu_izena_lc=lc($eremu_izena);
	my $path_edm=$path_zati_provcho."edm\:$eremu_izena";
	$nodeset = $xp->find($path_edm);
	print "\"edm_$eremu_izena_lc\":"."\"";
	foreach my $node ($nodeset->get_nodelist) 
	{   
	    my $str=$node->string_value; 
	    $str =~ s/^\s+|\s+$/ /g;
	    $str =~ s/\n//g;
	    print $str." "; # bat baino gehiago dagoenerako


	    # print $node->string_value;         
	}

	if($eremu_izena eq "type"){
	    print "\""."\n";
	}
	else
	{
	    print "\","."\n";
	}
    }


    # Ondorengo eremuak ez dut uste EDMetatik jasotzen direnik: paths_bow,paths_facet,date,paths_informativeness,paths_trav_count
    #idxfti


  print "}";   #BUKATU  FIELDS
  print "\n";
  print "},";   #BUKATU  ITEMA   !! kontuz azkeneko komakin !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  print "\n";
  $pk++;
}

 print "]"; #BUKATU    ITEM ZERRENDA   


=pod
[
  {
    "model": "myapp.person",
    "pk": 1,
    "fields": {
      "first_name": "John",
      "last_name": "Lennon"
    }
  },
  {
    "model": "myapp.person",
    "pk": 2,
    "fields": {
      "first_name": "Paul",
      "last_name": "McCartney"
    }
  }
]
=cut






=pod
my $dir=$ARGV[0];
my   $OS_ERROR; 
 
foreach my $fp (glob("$dir/*.xml")) {
  printf "%s\n", $fp;
  open my $XML, "<", $fp or die "can't read open '$fp': $OS_ERROR";
  my $XML2JSON = XML::XML2JSON->new();
  my $JSON = $XML2JSON->convert($XML);
  close $XML or die "can't read close '$XML': $OS_ERROR";

  print $JSON;
}

=cut
