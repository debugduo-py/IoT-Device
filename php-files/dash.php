<?php
$conn = mysqli_connect("localhost", "root", "","");

// if(!$conn){
// 	echo "connection not successful";
// }
// else{
// 	echo "connection successful";
// }



mysqli_query($conn,"CREATE DATABASE IF NOT EXISTS data_machine");
mysqli_select_db($conn,"data_machine");

$tablee = mysqli_query($conn,"CREATE TABLE IF NOT EXISTS station_details(
  date varchar(100) not null,
                       station_id varchar (100),
                       machine_id varchar (100),
                       quantity int
)");

mysqli_query($conn,"ALTER TABLE station_details MODIFY quantity int");

$devices_tab = mysqli_query($conn,"CREATE TABLE IF NOT EXISTS devices(
  machine_id varchar(100),
                            station_id varchar(100)
)");


$total_record = mysqli_fetch_assoc(mysqli_query($conn, "SELECT COUNT(*) AS full FROM station_details"));

$total_quan = mysqli_fetch_assoc(mysqli_query($conn,"SELECT sum(quantity) AS full FROM station_details"));

$machine_unique = mysqli_fetch_assoc(mysqli_query($conn, "SELECT COUNT(DISTINCT machine_id) AS full FROM station_details"));

$station_unique = mysqli_fetch_assoc(mysqli_query($conn, "SELECT COUNT(DISTINCT station_id) AS full FROM station_details"));
?>

<!DOCTYPE html>
<html>

<head>
<title>IoT Control Panel</title>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@300;400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles-light.css">

</head>
<body>

<div class="bg-grid"></div>

<aside class="sidebar">
<div class="sidebar-logo">
<div class="logo-dot"></div>
<span>IoT Panel</span>
</div>
<nav class="sidebar-nav">
<a href="#feature6" class="nav-item">Live Stats</a>
<a href="#feature5" class="nav-item"> All Data</a>
<a href="#feature10" class="nav-item"> Registered Devices</a>
<a href="#feature9" class="nav-item"> Quantity Range</a>
<a href="#feature1" class="nav-item"> Search by Date</a>
<a href="#feature2" class="nav-item"> Filter by ID</a>
<a href="#feature3" class="nav-item"> Add Record</a>
<a href="#feature4" class="nav-item nav-danger"> Delete Record</a>
<a href="#feature8" class="nav-item"> Machine Activity</a>
<a href="#feature7" class="nav-item"> Latest 5</a>

</nav>

</aside>
<main class="main">
<h1>IoT Control Panel</h1>

 <h2 id="feature6">Live stats</h2>
        <p> Total Records :
        <?php
        echo $total_record['full'];
        ?>
        </p>

        <p> Total Quantity :
        <?php
        echo $total_quan['full'];
        ?>
        </p>

        <p> Total Machines :
        <?php
        echo $machine_unique['full'];
        ?>
        </p>

        <p> Total Stations :
        <?php
        echo $station_unique['full'];
        ?>
        </p>





      <h2 id="feature5">All Records</h2>
      <?php

      $valuess = ['date', 'machine_id', 'station_id', 'quantity'];

      if (isset($_GET['sort']) && in_array($_GET['sort'], $valuess)) {
        $sorting = $_GET['sort'];
      }
      else{
        $sorting = 'date';
      }

      $res6 = mysqli_query($conn,"SELECT *FROM station_details ORDER BY $sorting");
      ?>




      <table>

      <tr>
      <th>
      <a href="?sort=date">Date</a>
      </th>

      <th>
      <a href="?sort=machine_id">Machine ID</a>
      </th>
      <th>
      <a href="?sort=station_id">Station ID</a>
      </th>
      <th>
      <a href="?sort=quantity">Quantity</a>
      </th>
      </tr>

      <?php while($row = mysqli_fetch_assoc($res6))
      {
        ?>
        <tr>
        <td>
        <?php
        echo $row['date'];
        ?>
        </td>
        <td>
        <?php
        echo $row['machine_id'];
        ?>
        </td>
        <td>
        <?php
        echo $row['station_id'];
        ?>
        </td>
        <td>
        <?php
        echo $row['quantity'];
        ?>
        </td>
        </tr>
        <?php } ?>
        </table>





                <h2 id = "feature10">Registered Devices
                </h2>





                <?php
                $res10 = mysqli_query($conn,"SELECT *FROM devices");

                ?>


                <table>
                <tr>

                <th>
                Machine ID
                </th>

                <th>
                Station ID
                </th>

                </tr>

                <?php while($row = mysqli_fetch_assoc($res10))
                { ?>
                  <tr>
                  <td>
                  <?php echo $row['machine_id'];
                  ?>

                  </td>
                  <td>
                  <?php echo $row['station_id'];
                  ?>

                  </td>

                  </tr>
                  <?php } ?>
                  </table>





            <h2 id = "feature9">Quantity Range Filter</h2>

            <form method = "POST">
            MIN:<input type = "text" name = "min" placeholder = "10"><br><br>

            MAX:<input type = "text" name = "max" placeholder = "30"><br><br>

            <input type = "submit" name = "max_check" value = "ENTER">
            </form>

            <?php
            if (isset($_POST['max_check'])) {
              $min = $_POST['min'];
              $max = $_POST['max'];

              $res9 = mysqli_query($conn,"SELECT * FROM station_details WHERE quantity BETWEEN $min AND $max");
              ?>

              <table>
              <tr>
              <th>
              Date
              </th>

              <th>
              Machine ID
              </th>

              <th>
              Station ID
              </th>

              <th>
              Quantity
              </th>
              </tr>

              <?php while($row = mysqli_fetch_assoc($res9))
              { ?>
                <tr>
                <td>
                <?php echo $row['date'];
                ?>

                </td>
                <td>
                <?php echo $row['machine_id'];
                ?>

                </td>
                <td>
                <?php echo $row['station_id'];
                ?>

                </td>
                <td>
                <?php echo $row['quantity'];
                ?>

                </td>
                </tr>
                <?php } ?>
                </table>

                <?php } ?>





  <h2 id="feature1">Search by date and time</h2>
  <form method = "POST">
  FROM : <input type = "text" name = "start" placeholder="2026-05-07 19:00:00">
  TO : <input type = "text" name = "end" placeholder="2026-05-07 19:00:00"><br><br>
  <input type = "submit" name = "check" value = "ENTER">
  </form>

  <?php
  if(isset($_POST['check'])){
    $from = $_POST['start'];
    $To = $_POST['end'];
    $res2 = mysqli_query($conn,"SELECT * FROM station_details WHERE date BETWEEN '$from' AND '$To'");
    ?>
    <table>
    <tr>
    <th>Date</th>
    <th>Machine ID</th>
    <th>Station ID</th>
    <th>Quantity</th>
    </tr>
    <?php while($row = mysqli_fetch_assoc($res2)){

      ?>
      <tr>
      <td>
      <?php echo $row['date'];
      ?>

      </td>
      <td>
      <?php echo $row['machine_id'];
      ?>

      </td>
      <td>
      <?php echo $row['station_id'];
      ?>

      </td>
      <td>
      <?php echo $row['quantity']; ?>

      </td>
      </tr>
      <?php } ?>
      </table>
      <?php
  }
  ?>




  <h2 id="feature2">Filter by Machine ID / Station ID</h2>
  <form method = "POST">
  Machine ID: <input type="text" name="machine_id">

  Station ID: <input type="text" name="station_id"><br><br>

  <input type = "submit" name = "verify" value = "ENTER">
  </form>

  <?php
  if(isset($_POST['verify'])){
    $machine = $_POST['machine_id'];
    $station = $_POST['station_id'];
    $res3 = mysqli_query($conn,"SELECT * FROM station_details WHERE machine_id='$machine' AND station_id='$station'");
    ?>
    <table>
    <tr>
    <th>Date</th>
    <th>Machine ID</th>
    <th>Station ID</th>
    <th>Quantity</th>
    </tr>
    <?php while($row = mysqli_fetch_assoc($res3))
    { ?>
      <tr>
      <td>
      <?php echo $row['date'];
      ?>

      </td>
      <td>
      <?php echo $row['machine_id'];
      ?>

      </td>
      <td>
      <?php echo $row['station_id'];
      ?>

      </td>
      <td>
      <?php echo $row['quantity'];
      ?>

      </td>
      </tr>
      <?php } ?>
      </table>
      <?php } ?>

      <h2 id="feature3">Add new record</h2>
      <form method="POST">
      DATE : &nbsp;&nbsp;
      <input type="text" name="datee"><br>

      MACHINE ID : &nbsp;&nbsp;
      <input type="text" name="machinee"><br>

      STATION ID : &nbsp;&nbsp;
      <input type="text" name="stationn"><br>

      QUANTITY : &nbsp;&nbsp;
      <input type="text" name="Quantityy"><br><br>

      <input type="submit" name="filter" value="ENTER">
      </form>
      <?php
      if (isset($_POST['filter'])) {
        $date = $_POST['datee'];

        $machine_idd = $_POST['machinee'];

        $station_idd = $_POST['stationn'];

        $Quant = $_POST['Quantityy'];

        $res4 = mysqli_query($conn,"INSERT INTO station_details (date, machine_id, station_id, quantity) VALUES('$date','$machine_idd','$station_idd','$Quant')");

        if ($res4) {
          echo "Record added successfully";
        }
        else{
          echo "Error adding a record";
        }
      }
      ?>



      <h2 id="feature4">Delete a record </h2>
      <form method = "POST">
      DATE : <input type = "text" name = "del" placeholder = "2026-05-07 19:00:00"><br><br>
      <input type = "submit" name = "fil" value = "ENTER">
      </form>

      <?php
      if (isset($_POST['fil'])) {
        $del = $_POST['del'];
        $res5 = mysqli_query($conn,"DELETE FROM station_details WHERE date = '$del' LIMIT 1");
        if ($res5) {
          echo "record deleted successfully";
        }
        else{
          echo "Error:".mysqli_error($conn);
        }
      }

      ?>





        <h2 id = "feature7">5 Latest Records</h2>

        <?php
        $res7 = mysqli_query($conn,"SELECT * FROM station_details ORDER BY date DESC LIMIT 5");
        ?>

        <table>
        <tr>
        <th>
        Date
        </th>

        <th>
        Machine ID
        </th>

        <th>
        Station ID
        </th>

        <th>
        Quantity
        </th>
        </tr>

        <?php while($row = mysqli_fetch_assoc($res7))
        { ?>
          <tr>
          <td>
          <?php echo $row['date'];
          ?>

          </td>
          <td>
          <?php echo $row['machine_id'];
          ?>

          </td>
          <td>
          <?php echo $row['station_id'];
          ?>

          </td>
          <td>
          <?php echo $row['quantity'];
          ?>

          </td>
          </tr>
          <?php } ?>
          </table>


          <h2 id = "feature8">Feature 8 —> Machine Activity</h2>

          <?php
          $res8 = mysqli_query($conn,"SELECT machine_id, COUNT(*) AS tot_records,SUM(quantity) AS tot_quan FROM station_details GROUP BY machine_id");
          ?>
          <table>
          <tr>
          <th>Machine ID</th>
          <th>Total Records</th>
          <th>Total Quantity</th>
          </tr>

          <?php while($row = mysqli_fetch_assoc($res8))
          { ?>
            <tr>
            <td>
            <?php echo $row['machine_id'];
            ?>

            </td>

            <td>
            <?php echo $row['tot_records'];
            ?>
            </td>

            <td>
            <?php echo $row['tot_quan'];
            ?>
            </td>
            </tr>
            <?php } ?>
            </table>

            <!-- HOW THIS WILL WORK IS
            EG: suppose
            M1 : 10
            M1 : 20
            M2 : 50

            AFTER THE QUERY WHAT WILL HAPPEN IS
            IT WILL SORT AS
            MACHINE ID | TOTAL RECORDS | TOTAL QUANTITY
            M1         |2              |30
            M2         |1              |50

            -->


                  </main>
                  </body>
                  </html>
