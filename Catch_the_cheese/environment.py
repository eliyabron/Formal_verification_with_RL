from numpy import random, size
from action import Action
import numpy as np
from copy import deepcopy
from numpy.random import seed
from numpy.random import randint
import random
import parameters_run
SIZE=parameters_run.get_size()
NUM_HOLES=1


class Environment:

    def __init__(self):
        #write the map
        self.map=['H']
        for i in range (1,SIZE-1):
            self.map.append('F')
        self.map.append('C')
        
        self.index_hole=[0]
        
        
        
        self.action_space = np.array([Action.Left, Action.Right])
        self.state_space = [i for i in range(np.array(self.map).size)]

        self.current_state = 20
        self.score=0
    def get_holes(self):
        return self.index_hole

    def get_action_space(self):
        return self.action_space

    def get_state_space(self):
        return self.state_space

    def get_random_action(self):
        return np.random.choice(self.action_space)


    def step(self, action_index):
        action = Action(action_index)

        if self.invalid_action(action):
            return self.current_state, -10*SIZE*SIZE, False

        if action == Action.Left:
            self.current_state -= 1
        elif action == Action.Right:
            self.current_state += 1
        
        
        letter = self.map[self.current_state]

       
        
        if letter == 'F':
             return self.current_state, -SIZE, False
        if letter == 'C' and self.score<5:
            self.score+=1
            return self.current_state, 100*SIZE*SIZE, False
        if letter == 'C' and self.score>=parameters_run.get_score():
            return self.current_state, 10010*SIZE*SIZE, True
        else:
            return self.current_state, -10*SIZE*SIZE, True


    def invalid_action(self, action):
        if (action == Action.Left and self.current_state==0) or \
           (action == Action.Right and self.current_state==(SIZE-1)): 
           
           return True

        return False
    

    def reset(self):
        self.current_state = parameters_run.get_start_point()
        self.score=0
        return self.current_state

    def print_current_state(self):
        temp_map = deepcopy(self.map)
        for i in range(0,SIZE):
            if self.current_state!=i:
                if(temp_map[i]=='F'):
                    print('.', end =" " )
                if(temp_map[i]=='H'):
                    print('O', end =" " )
                if(temp_map[i]=='C'):
                    print('C', end =" " )
                if(temp_map[i]=='S'):
                    print('S', end =" " )
            else:
                print('X', end =" " )
            
        print()
        print()