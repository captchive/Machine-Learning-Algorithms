$classifierFile = shift;
$dir = shift;
$data = shift;
$mean = 0;

for(my $i=0; $i<10; $i++){
  system("python $classifierFile $dir/$data/$data.data $dir/$data/$data.trainlabels.$i > nm_out.$data");
  $err[$i] = `perl error.pl $dir/$data/$data.labels nm_out.$data`;
  chomp $err[$i];
  print "$err[$i]\n";
  $mean += $err[$i];
}
$mean /= 10;
$sd = 0;
for(my $i=0; $i<10; $i++){
  $sd += ($err[$i]-$mean)**2;
}
$sd /= 10;
$sd = sqrt($sd);
print "Classifier error(mean, (std)) = $mean ($sd)\n";
