 <?php
 header("Content-type: text/html; charset=utf-8");
require_once('../include/db_info.inc.php');
if(isset($_GET['id'])){
    $id=$_GET['id']-1000;
    $result =mysql_query("select pid2,(select title from problem where problem_id=pid2+1000) title , sim from problem_sim  where pid1 ='$id' ORDER BY sim DESC limit 20 OFFSET 1 ") or die(mysql_error());
    $output=array();
    $i=0;
   while($row=mysql_fetch_row($result)){
        if(rand(0,100)>30){ //top20中随机选择5题目，返回到前台
         $output[]=array($row[0]+1000,$row[1],$row[2]);
         if(++$i==5)break;
        }
    }
   echo json_encode($output);
}             
?>