<?php
    $fn = $_GET['f'] . '.json';
    $remove = $_GET['d'];
    $file = file_get_contents($fn);
    $json = json_decode($file, true);

    for ($i=0; $i < count($json); $i++) { 
        $item = $json[$i];
            
        if ($item["date"] == $remove) {
            unset($json[$i]);
            break;
        }
    }
    $json = array_values($json);
    file_put_contents($fn, json_encode($json));
?>