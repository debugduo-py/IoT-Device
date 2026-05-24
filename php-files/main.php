    <?php
        echo "oui, je suis le server";

        $conn = mysqli_connect('localhost', 'root', '', '');
        //name of database
        $creation = mysqli_query($conn,"CREATE DATABASE IF NOT EXISTS data_machine");
        $sql = mysqli_select_db($conn,"data_machine");

        //structure of database, change if u want bt it should match to wt u had set in the python file
        //------------------------------------------------------------------------
        $table = mysqli_query($conn,"CREATE TABLE IF NOT EXISTS station_details(
            date varchar(100) PRIMARY KEY,
            machine_id int,
            station_id int,
            quantity int
            )");
        //------------------------------------------------------------------------

        $main = json_decode($_POST['message'],true);

        if ($main['machine_id'] != null) {
            $query = "INSERT INTO station_details VALUES ('".date("Y-m-d H:i:s")."','".$main['machine_id']."', '".$main['station_id']."','".$main['quantity']."')";
            $result = mysqli_query($conn,$query);

            if ($result) {
                echo "success";
            }

        }
        ?>
