import parameters_run
from environment import Environment
from q_learning import Q_Learning
from utils import runSmv, writeSmv
import numpy as np
import matplotlib.pyplot as plt

def main():
    DictResults={}
    DictResults["Converged ,with NuXmv"]=0
    DictResults["Did not converged ,with NuXmv"]=0
    DictResults["Converged ,without NuXmv"]=0
    DictResults["Did not converged,without NuXmv"]=0
    num_games=40
    switch=int(num_games/2)
    for i in range(num_games):
        get_the_cheese = Environment()
        q_learning_algo = Q_Learning(get_the_cheese)
        if i<switch:
          q_learning_algo.setuseNusmv(1)
        if i>=switch:
          q_learning_algo.setuseNusmv(0)
        
        q_learning_algo.run_algorithm()

        Q=q_learning_algo.getQ()
        H=get_the_cheese.get_holes()

        
        #q_learning_algo.print_results()
        r=q_learning_algo.run_and_print_latest_iteration()
        if r==0 and i>=switch:
           DictResults["Did not converged,without NuXmv"]+=1
        if r==0 and i<switch:
           DictResults["Did not converged ,with NuXmv"]+=1
        if r==1 and i>=switch:
           DictResults["Converged ,without NuXmv"]+=1
        if r==1 and i<switch:
           DictResults["Converged ,with NuXmv"]+=1
        
    width = 0.1 
    
    plt.bar(DictResults.keys(), DictResults.values(),width)
    plt.ylabel('Games') 
  
  # displaying the title
    plt.title(str(num_games)+" games of Catch the cheese")
    plt.show()



if __name__ == '__main__':
    main()