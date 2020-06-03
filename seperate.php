<?php


function read_file() {
	$path = 'Todelivery_US_01_06.csv';
	$fp = fopen($path, 'r');
	$wf = fopen('sep.csv', 'a');
	$count = 0;
	while (! feof($fp)) {
		$record = fgetcsv($fp);
		if (count($record) === 5){
			$new = [explode(' ', $record[0])[0], explode(' ', $record[0])[1], $record[1], $record[2], $record[3], $record[4]];
		} elseif (count($record) === 4) {
			$sep = explode(' ', $record[0]);
			if (count($sep) === 2) {
				$new = [$sep[0], $sep[1], $record[1], $record[2], $record[3]];
			} else {
				echo "Just First Name\n";
				$new = [$sep[0], '', $record[1], $record[2], $record[3]];
			}
		} else {
			echo "Oops, OMG\n";
		}
		fputcsv($wf, $new);
		$count += 1;
		echo $count."\n";
	}
	fclose($fp);
	fclose($wf);
}

function main() {
	read_file();
}

main();
?>