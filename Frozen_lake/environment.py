from numpy import random, size
from action import Action
import numpy as np
from copy import deepcopy
from numpy.random import seed
from numpy.random import randint
import random
import parameters_run
SIZE=parameters_run.get_size()
NUM_HOLES=int(SIZE*SIZE/8)
#random.seed(0)

class Environment:

    def __init__(self):
        #write the map
        self.map=['S']
        for i in range (1,SIZE*SIZE-1):
            self.map.append('F')
        self.map.append('G')
        direction=1
        self.index_hole=[]
        
        #self.index_hole=random.sample(range((2),(SIZE*SIZE-3)), NUM_HOLES)
        #for i in self.index_hole:
            #self.map[i]='H'
        """
        for i in range(SIZE):
          if i%2==1:
           if direction==1:
             for j in range(SIZE-2):
              self.index_hole.append((i)*SIZE+j)
              self.map[(i)*SIZE+j]='H'
             direction=2
           else:
             for j in range(SIZE-2):
              self.index_hole.append((i)*SIZE+SIZE-j-1)
              self.map[(i)*SIZE+SIZE-j-1]='H'
             direction=1
          """
        for i in range(SIZE):
             for j in range(SIZE):
              self.index_hole.append((i)*SIZE+j)
              self.map[(i)*SIZE+j]='H'
             
        for i in range(SIZE):
                self.map[i]='F'
                if i in self.index_hole:
                 self.index_hole.remove(i)
        for i in range(SIZE):
            self.map[i*SIZE+SIZE-1]='F'
            if i+SIZE-1 in self.index_hole:
                 self.index_hole.remove(i*SIZE+SIZE-1)
        self.map[(SIZE)*SIZE-1]='H'
            
        
        self.action_space = np.array([Action.Left, Action.Right, Action.Up, Action.Down])
        self.state_space = [i for i in range(np.array(self.map).size)]

        self.current_state = 0

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
        elif action == Action.Up:
            self.current_state -= SIZE
        else:
            self.current_state += SIZE
        
        letter = self.map[self.current_state]

       
        if letter == 'S':
            return self.current_state, -10*SIZE*SIZE, False
        if letter == 'F':
             return self.current_state, -SIZE, False
        elif letter == 'G':
            return self.current_state, 100*SIZE*SIZE, True
        else:
            return self.current_state, -10*SIZE*SIZE, True


    def invalid_action(self, action):
        if (action == Action.Left and self.current_state%SIZE==0) or \
           (action == Action.Right and self.current_state%(SIZE)==(SIZE-1)) or \
           (action == Action.Up and self.current_state<SIZE) or \
           (action == Action.Down and (SIZE*SIZE-SIZE)<=self.current_state and self.current_state<=SIZE*SIZE-1):
            return True

        return False
    

    def reset(self):
        self.current_state = 0
        return self.current_state

    def print_current_state(self):
        temp_map = deepcopy(self.map)
        for i in range(0,SIZE*SIZE):
            if self.current_state!=i:
                if(temp_map[i]=='F'):
                    print('.', end =" " )
                if(temp_map[i]=='H'):
                    print('O', end =" " )
                if(temp_map[i]=='G'):
                    print('G', end =" " )
                if(temp_map[i]=='S'):
                    print('S', end =" " )
            else:
                print('X', end =" " )
            if i%SIZE==(SIZE-1):
                print()
        print()
        print()