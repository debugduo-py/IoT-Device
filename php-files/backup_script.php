    <?php

        $conn = mysqli_connect('localhost', 'root', '', 'data_machine');

        $info = json_decode($_POST['message'],true);



        $main = json_decode($info[1],true);

        // echo $info[0];
        // echo $main['machine_id'];
        // echo $main['station_id'];
        // echo $main['quantity'];
        if ($main['machine_id'] != null) {
            $query = "INSERT INTO station_details VALUES ('".$info[0]."','".$main['machine_id']."', '".$main['station_id']."','".$main['quantity']."')";
            echo $query;
            $result = mysqli_query($conn,$query);

            if ($result) {
                echo "success";
            }
            else{
                echo $query;
            }

        }
        ?>
