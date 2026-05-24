<?php

    echo "This is devices.php ";

    $conn = mysqli_connect('localhost', 'root', '', '');
    //name of database
    $creation = mysqli_query($conn,"CREATE DATABASE IF NOT EXISTS data_machine");
    $sql = mysqli_select_db($conn,"data_machine");

    //structure of database, change if u want bt it should match to wt u had set in the python file
    //------------------------------------------------------------------------
    $table = mysqli_query($conn,"CREATE TABLE IF NOT EXISTS devices(

        machine_id int,
        station_id int,
        primary key(machine_id,station_id)
        )");
    //------------------------------------------------------------------------

    $main = json_decode($_POST['message'],true);

    $deletable = json_decode($_POST['removal'],true);

    if ($deletable['machine_id'] != null) {
        echo "not null";
        $result1 = mysqli_query($conn,"
            DELETE FROM devices
            WHERE machine_id = ".$deletable['machine_id']."
            AND
            station_id = ".$deletable['station_id']."

            ");
        if ($result1) {
            echo "success";
        }
    }

    echo "decoded the json data";

    echo "recieved --> ".$main['machine_id'];

    if ($main['machine_id'] != null) {

        $check = mysqli_query($conn,"
            SELECT * FROM devices where
            machine_id = ".$main['machine_id']."
            and
            station_id = ".$main['station_id']."

            ");

        echo "checking for query";

        if (mysqli_num_rows($check) != 0) {
            echo "exists";
        }
        else {
            $a = mysqli_query($conn,"
            DELETE FROM devices where
            machine_id = ".$main['machine_id_old']."
            and
            station_id = ".$main['station_id_old']."

            ");

            if ($a) {
                echo "____OLD DATA REMOVED SUCCESSFULLY____";
            }

            $result = mysqli_query($conn,"
                INSERT INTO devices VALUES
                (".$main['machine_id'].",".$main['station_id'].")
                ");

            if ($result) {
                echo "success";
            }
            else{
                echo "query failed";
            }


        }



    }
    ?>

