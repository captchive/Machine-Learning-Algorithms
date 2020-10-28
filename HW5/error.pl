$true=shift;
open(IN,$true);
while(<IN>){
   chomp $_;
   @s=split(/\s+/,$_);
   $truelabels{$s[1]}=$s[0];
} close IN;
#foreach my $x (keys %truelabels) { print "$x $truelabels{$x}\n"; }
$predict=shift;
open(IN,$predict);
while(<IN>){
  chomp $_; @s=split(/\s+/,$_);
  if(defined($truelabels{$s[1]})) {
     $predictedlabels{$s[1]}=$s[0];
  }
} close IN;
#foreach my $x (keys %predictedlabels) { print "$x $predictedlabels{$x}\n"; }
$size=keys %predictedlabels;
#print "size= $size\n";
$error=0;
$a=0;$b=0;$c=0;$d=0;
foreach my $x (keys %predictedlabels) {
   if($truelabels{$x} == 0 && $predictedlabels{$x} == 0) { $a++; }
   if($truelabels{$x} == 0 && $predictedlabels{$x} == 1) { $b++; $error++; }
   if($truelabels{$x} == 1 && $predictedlabels{$x} == 0) { $c++; $error++; }
   if($truelabels{$x} == 1 && $predictedlabels{$x} == 1) { $d++; }
}
#print "a=$a b=$b c=$c d=$d\n";
$BER = 0.5*($b/($a+$b) + $c/($c+$d));
$errorRate=$error/$size;
print "$BER\n";
#print "$errorRate\n";