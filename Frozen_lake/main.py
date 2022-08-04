from inspect import Parameter
from environment import Environment
from q_learning import Q_Learning
from utils import runSmv, writeSmv
import numpy as np
import matplotlib.pyplot as plt
import parameters_run
#need to change size only on envioremnt, and utils (if used)

def main():
    X = ['Converged ,with NuXmv','Did not converged ,with NuXmv','Converged ,without NuXmv','Did not converged,without NuXmv']
    size10=[0,0,0,0]
    size20=[0,0,0,0]
    DictResults={}
    DictResults["Converged ,with NuXmv"]=0
    DictResults["Did not converged ,with NuXmv"]=0
    DictResults["Converged ,without NuXmv"]=0
    DictResults["Did not converged,without NuXmv"]=0
    num_games=40
    switch=int(num_games/2)
    for s in range(2):
        if s==0:
           parameters_run.set_size(10) 
           
        if s==1:
           parameters_run.set_size(20)
        for i in range(num_games):
            frozen_lake_environment = Environment()
            q_learning_algo = Q_Learning(frozen_lake_environment)
            if i<switch:
              q_learning_algo.setuseNusmv(1)
            if i>=switch:
              q_learning_algo.setuseNusmv(0)
        
            q_learning_algo.run_algorithm()

            Q=q_learning_algo.getQ()
            H=frozen_lake_environment.get_holes()

            #q_learning_algo.print_results()
            r=q_learning_algo.run_and_print_latest_iteration()
            if r==0 and i>=switch:
              if s==0:
                size10[3]+=1
              if s==1:
                size20[3]+=1
           
            if r==0 and i<switch:
              if s==0:
                size10[1]+=1
              if s==1:
                size20[1]+=1
            if r==1 and i>=switch:
             if s==0:
                size10[2]+=1
             if s==1:
                size20[2]+=1
            if r==1 and i<switch:
              if s==0:
                size10[0]+=1
              if s==1:
                size20[0]+=1
        
    X_axis = np.arange(len(X))
  
    plt.bar(X_axis - 0.1, size10, 0.1, label = 'size 10x10')
    plt.bar(X_axis + 0.1, size20, 0.1, label = 'size 20x20')
  
    plt.xticks(X_axis, X)
    plt.ylim(0,max(size10)+4)
    plt.ylabel("Number of games")
    plt.title(str(num_games)+" games of frozen lake for boards 10x10,20x20")
    plt.legend()
    plt.show()






if __name__ == '__main__':
    main()