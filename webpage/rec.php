<?php
header("Content-type: text/html; charset=utf-8");
require_once('../include/db_info.inc.php');

$problem_start_number=1000;
if (isset($_GET['user_id'])){
     $user_id=$_GET['user_id'];
}else if (isset($_SESSION['user_id'])){
     $user_id=$_SESSION['user_id'];
}
if($user_id){
   //echo $user_id; 
//1. 获取用户所有提交的题目 和 最近提交50道题
$sql =mysql_query("select DISTINCT problem_id from solution where user_id='$user_id' 
 order by solution_id  desc") or die(mysql_error());
$n=50;
$last_n_done= array(); //记录最近n次提交的题目
$user_n_done_str="1000";//用户最后提交的n道题拼成一个串
$i=0;
$user_done= array();  //记录用户所有提交的题目
$delim=",";
while($row=mysql_fetch_row($sql)){
        $problem_id=intval($row[0])-$problem_start_number;// the problem number start from 1000
        if(++$i<=$n){
            $last_n_done[]=$problem_id;// 从0开始计数
            $user_n_done_str.=$delim.$problem_id;
        }
        $user_done[]=$problem_id;
}
//echo $user_n_done_str;
// 2.获取题目的相似度矩阵 编号是实际题目编号
$sql=mysql_query("select * from problem_sim  where pid1 in ($user_n_done_str)") or die(mysql_error());
$sim_problem=array();
while($row=mysql_fetch_array($sql)){
        if(!isset($sim_problem[$row[0]])) $sim_problem[$row[0]]=array();
        $sim_problem[$row[0]][$row[1]]=$row[2];
}
$filte = array();
$dscore= array();//对ac次数较多的题目进行减分处理
// 题目id,该题的总ac数, 是否可见, 标题
$sql=mysql_query("select problem_id,accepted,defunct,title from problem ") or die(mysql_error());
$ptitle=array(); // 记录第i道题的名字
while($row=mysql_fetch_row($sql)){
       $pid=intval($row[0])-$problem_start_number;
       $ac=intval($row[1]);
       $title=$row[3];
       if( $row[2] == "Y" || $ac<2) $filte[]=$pid; // 不可见的题目或者ac数小于2的 放入过滤数组
       if($ac==0) $ac=20;
       $dscore[$pid]= 1.0/log($ac+1,2);
       $ptitle[$pid]=$title;
}
//选出我最后提交的n道题，每道题所对应的相关度最高的100道，按照相同题号(列)累加到result。
$result= array();
if($last_n_done)foreach($last_n_done as $i=>$pid1){
     if($sim_problem[$pid1]) foreach($sim_problem[$pid1] as $pid2=>$sim){
            if(!isset($result[$pid2])) $result[$pid2]=0;
            $result[$pid2] += $sim*$dscore[$pid1]/log($i+2,2);
     }
}
// 过滤 filte[]列表的题目
if($filte)foreach($filte as $pid){
        $result[$pid]=0;
}
// 过滤用户提交的题目
if($user_done) foreach($user_done as $pid){
        $result[$pid]=0;
} 
//过滤正在contest中的题目
$sql=mysql_query("SELECT DISTINCT `problem_id` FROM `contest_problem` WHERE `contest_id` IN (SELECT `contest_id` FROM `contest` WHERE `end_time`>NOW()  and `defunct`='N')") or die(mysql_error());
while($row=mysql_fetch_row($sql)){
       $pid=intval($row[0])-$problem_start_number;
       if($pid>=0)$result[$pid]=0;
}            
//计算出的用户推荐矩阵，取top 20打包，返回到页面
arsort($result);
$output=array();
$i=0;
foreach ($result as $pid =>$sim){
       if(rand(0,100)>30){ //top20中随机选择5题目，返回到前台
        if(++$i>10) break;
        $output[]=array($pid+1000,$ptitle[$pid],$sim);
       }
}
//返回
  echo json_encode($output);
}   
?>