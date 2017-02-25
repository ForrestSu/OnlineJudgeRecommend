#!/usr/bin/env python
# coding=utf-8
import scipy.sparse as sp
import sys
import numpy
import unittest
 
#功能就是求相似度，传入一个矩阵，算出行维度的余弦相似度。
#过程
#1.求出每行的平方和，得到一个m*1的矩阵b。  B*B.T得到分母的平方的矩阵  [m*m]   
#2.输入矩阵(m*n)乘以输入矩阵的转置(n*m)，得到一个m*m的矩阵
#3.用第二步中m*m的矩阵每行的每个元素除以第一步中m*m矩阵中每行的对应元素。

def get_cosine_sim(matrix):
    sq_sum = numpy.multiply(matrix, matrix).sum(1) # 矩阵每个元素平方，然后按行求和，变成一个m*1的列矩阵
    sq_sum = sq_sum * sq_sum.T      #(m*1)列矩阵*(1*m)行矩阵=>  m*m矩阵  
    matrix = sp.csc_matrix(matrix)          # =>稀疏matrix
    matrix = (matrix * matrix.T).todense()  # 叉积(向量积) ,将稀疏矩阵转化为完整特征矩阵 
    numpy.divide(matrix, numpy.power(sq_sum, 0.5,sq_sum), matrix)
    return matrix

# this is not used ..
# because the matrix is not a sparse matrix any more after adjusted
#def get_adjusted_cosine_sim(matrix):
#    matrix -= matrix.mean(0)
#    return get_cosine_sim(matrix)

# need a dense matrix, return a csc_matrix需要一个稠密矩阵，返回一个csc_matrix(Compressed Sparse Column matrix)压缩稀疏列矩阵
# k neareast neibour .. will modify the sim_problem
'''
保留传入矩阵中每行的前k+1个大元素，其它元素全部置0。（为啥是k+1而不是k个，主要是我想着k个最近邻居加上自己嘛）
这里主要是为了将前一步计算出的矩阵变成一个稀疏矩阵，一是后面的计算比较快，二是去除一些相关度离得比较远的东东。
'''
def knn(sim_problem, k):
    size = sim_problem.shape[1]   # shape[0]求矩阵的行数,shape[1]求矩阵的列数。 为题目数m
    sim_problem[sim_problem<sim_problem[range(0,size),sim_problem.argsort()[:, size - k -1].T].T.repeat(size, 1)]=0
    return sim_problem

def get_recommend_matrix( sim_problem,last_50_submit):
    matrix=sim_problem.sum(1)      # sum(0)按列求和，sum(1)按行求和， 变成一维列矩阵
    problem_user = (sp.csc_matrix(sim_problem) * sp.csc_matrix(last_50_submit)).todense()
    matrix = numpy.divide(problem_user, matrix)
    return matrix

