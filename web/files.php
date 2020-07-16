<?php 
    $out = array();
    foreach (glob('*.json') as $filename) {
        $p = pathinfo($filename);
        $out[] = $p['filename'];
    }
    echo json_encode($out); 
?>
