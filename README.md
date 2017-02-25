
## OnlineJudgeRecommend
 An ACM problem recommendation module ! (Collaborative Filtering Algorithm, based on hustoj)    

## Requirements
* Python 2.7+ (Ubuntu 14.04)

## Introduction
 关于协同过滤的介绍，《集体智慧编程》第二章有详细的介绍。

## Screenshots
![RDM](https://github.com/ForrestSu/OnlineJudgeRecommend/blob/master/img/rec.png)

## Installation
1. Install [Python 2.7](https://www.python.org/downloads/)+

2. Install third library
> sudo apt-get install python-numpy  
sudo apt-get install python-scipy  
sudo apt-get install python-mysqldb

3. db
> use jol;
> create table problem_sim(
>    
> );

4. Download src
> git clone  https://github.com/ForrestSu/OnlineJudgeRecommend.git recommend

5. Modify Database Password in `recommend.py`.

6. AutoRun Everyday
> vi /etc/crontab    #系统每天6点30分执行recommend.py (crontab文件PATH后追加`/etc/recommend`)  
30 6    * * *   root    python /etc/recommend/recommend.py >> /etc/recommend/rec.log 2>&1

7. Modify HustOj front page 


## Author
[SunQuan](https://github.com/ForrestSu)

## Publications
 2015年06月，在**电脑与信息技术**上发表一篇小论文《协同过滤算法在ACM在线评测推荐系统中的应用研究》 
