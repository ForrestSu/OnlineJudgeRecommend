#!/usr/bin/env python
# coding=utf-8
'''
create table problem_sim
(
   pid1                 int not null,
   pid2                 int not null,
   sim                  double not null
);
'''
import numpy
import dbutil 
import rec
import time
#import unittest

#1.首先得检查 solution 中的user_id 在users 都存在
#2.检查 solution 中的problem_id 在problem 都存在 1730-1740
#3.题库里面必须有题目,且solution里面有提交记录
def load_last_n_correct(conn,n, udict):
    user_num=len(udict)               #用户数N，题目数M=650
    sql="select max(problem_id) from problem;"
    cnt=conn.query(sql);
    problem_num=int(cnt[0][0])-1000+5;
    user_solved_cnt=[0 for i in range(user_num)]             #user[N]，统计每个用户的A题数
    last_n_correct = [[0 for j in range(user_num)] for i in range(problem_num)]  #l[M][N]
    user_solved_problem = [[0 for j in range(user_num)] for i in range(problem_num)] # usp[M][N]
    sql="select problem_id,user_id  from solution where result=4  order by solution_id DESC;"
    resultSet=conn.query(sql);
    for line in resultSet:
        pid = int(line[0])-1000
        if(pid<0):
            print "error1",pid
            continue
        if(udict.has_key(line[1])):uid = udict[line[1]]
        else: 
            print "error2"
            continue
        if user_solved_problem[pid][uid] == 0: # 多次AC同一道题只算一次
            user_solved_problem[pid][uid] = 1    # 记录用户所有正确提交
            user_solved_cnt[uid] += 1            # 记录每个用户ac题目数量
            if (user_solved_cnt[uid] <= n): # # 只记录每一个用户最后AC的50次提交
                last_n_correct[pid][uid] = 1
                
    last_n_correct= numpy.matrix(last_n_correct,numpy.double)# 转成double类型的矩阵，没有逗号分隔
    return last_n_correct
#返回用户字典{name,id} 用户名列表
def load_user_dict(conn):
    sql="select user_id from users;"
    users=conn.query(sql);
    uid=0
    user_dict={}
    for one in users:
        user_dict[one[0]]=uid
        uid=uid+1;
    return user_dict

# sum(1)按行求和，sum(0)按列求和， 变成一维矩阵
#返回 problem[M]=[1/log2( 每道题AC的次+2)]
def get_user_done_score(user_matrix):
    user_matrix = numpy.matrix(user_matrix)
    done_score = numpy.divide([1],numpy.log2(user_matrix.sum(1) + 2))
    done_score[numpy.isinf(done_score)]=0  #一重循环，中间是条件
    return done_score
def insert_to_problem_sim(mysql,sim):
    sql=" delete from problem_sim;"
    print mysql.execute(sql)
    row=sim.shape[0]# row
    col=sim.shape[1]# col  
    params = [(i,j,sim[i,j]) for i in xrange(row) for j in xrange(col) if(sim[i,j]>0.0)]
    sql = "INSERT INTO `problem_sim`(`pid1`,`pid2`,`sim`) VALUES(%s,%s,%s);"   
    mysql.executemany(sql, params)
    sql="select count(*) from problem_sim;"
    cnt=mysql.query(sql);
    print 'insert',int(cnt[0][0]),'rows record';

start=time.time()
host='localhost' #'172.28.27.26'
passwd='asdfghjkl@123'
mysql=dbutil._MySQL(host,3306,'root',passwd,'jol')
#1.加载用户数据字典
udict=load_user_dict(mysql)  
data_matrix=load_last_n_correct(mysql,1000, udict)
#对做对的人太多的题目进行降分处理
#本来没加这条，结果不大好，经常会推荐一些大家都做的水题
#虽然也能解释通，就是大家都喜欢的一定是好的
#但是由于不太适用于OJ，就在这里做了过热惩罚。使用的公式是1/log2(n+1)
dscore=get_user_done_score(data_matrix)  # dscore[M] 一维数组dscore[M]=[1/log2( 每道题AC的次数n+1)](if n==0 then 0)

# 真正把原矩阵进行两种加权：难度加权（一维）、热度降权（一维）data_matrix每一列都会乘   
numpy.multiply(data_matrix,dscore,data_matrix)  # 每一列都乘以一个列矩阵，存储到data_matrix 并返回
 
#计算物品间的余弦相似度，这里我使用的是已经过热惩罚并且加权了难度的数据
# 实测表明似乎这里不加权这两样，对后面结果影响不太明显，不过加上应该是好些的。
sim=rec.get_cosine_sim(data_matrix)   #sim => m*m 的相似度矩阵 
#去掉上步发生除零错误时得到的nan
sim[numpy.isnan(sim)] = -1
#获取k个最近邻居
sim = rec.knn(sim,100)
mysql=dbutil._MySQL(host,3306,'root',passwd,'jol')
insert_to_problem_sim(mysql,sim)
end=time.time()
print "total cost:",end-start,"second" 
print time.strftime('--%Y-%m-%d %H:%M:%S--') # 打印当前时间
# about 13 seconds in windows
 
