import numpy as np
import random
import time
from utils import runSmv, writeSmv
import parameters_run
from environment import SIZE

class Q_Learning:

    def __init__(self, environment, **parameters):
        self.env = environment

        self.num_episodes = parameters.get('num_episodes', SIZE*1000)
        self.max_steps_per_episode = parameters.get('max_steps_per_episode', SIZE*SIZE)
        self.learning_rate = parameters.get('learning_rate', 0.1)
        self.discount_rate = parameters.get('discount_rate', 0.99)
        self.exploration_rate = parameters.get('exploration_rate', 1)
        self.max_exploration_rate = parameters.get('max_exploration_rate', 1)
        self.min_exploration_rate = parameters.get('min_exploration_rate', 0.01)
        self.exploration_decay_rate = parameters.get('exploration_decay_rate', 0.0001)

        self.bigChange=0
        self.epsilon=0.0000000000000000000000000001
        self.episodes=0

        self.q_table = np.zeros((len(environment.get_state_space()), len(environment.get_action_space())))
        self.all_episode_rewards = []
        self.useNusmv=parameters_run.get_useNusmv()
    def getQ(self):
        return self.q_table
    def setuseNusmv(self,value):
         self.useNusmv=value
    def run_algorithm(self):
        #FLAG_win shows wheter smv found a solution or not and what solution
        FLAG_win=False
        #maxSteps shows which number of steps we need to take to win 
        maxSteps=SIZE*SIZE+1

        finalanswer=[]

        for episode in range(self.num_episodes):
            rewards_for_current_episode = 0
            state = self.env.reset()

            old_q=self.q_table.copy()
            for step in range(self.max_steps_per_episode):
                rand = random.uniform(0, 1)
                if rand < self.exploration_rate:
                    action_index = self.env.get_random_action().value
                else:
                    action_index = np.argmax(self.q_table[state, :])

                new_state, reward, done = self.env.step(action_index)
                

                self.q_table[state][action_index] = self.q_table[state][action_index] * (1 - self.learning_rate) + \
                                                    self.learning_rate * (
                                                            reward + self.discount_rate * np.max(
                                                        self.q_table[new_state, :]))

                state = new_state
                rewards_for_current_episode += reward              

                if done:
                    break

            self.exploration_rate = self.min_exploration_rate + \
                                    (self.max_exploration_rate - self.min_exploration_rate) * np.exp(
                -self.exploration_decay_rate * episode)

            self.all_episode_rewards.append(rewards_for_current_episode)
            
            if episode%2000==0:
                print("we are in episode", episode)


            if (episode%100==0) and episode>0 and self.useNusmv==1:
                writeSmv(SIZE, maxSteps ,self.q_table, self.env.get_holes())
                answer=runSmv()
                
                if answer[1]==False:
                    self.q_table[answer[2]][answer[3]]= self.q_table[answer[2]][answer[3]]-1000
                    print(answer[0])
                    print(answer[1])
                    print(answer[2])
                    print(answer[3])
                    
                if answer[1]==True:
                    print("found something ", len(answer[0]))
                    FLAG_win=True
                    maxSteps=len(answer[0])

                    #print(answer[0])
                    for i in range(len(answer[0])-1):
                        n_state=answer[0][i]
                        new_state=answer[0][i+1]
                        
                        #left
                        if int(new_state)-int(n_state)==int(-1):
                            action_index=0
                        #right
                        elif int(new_state)-int(n_state)==int(1):
                            action_index=1
                        #up
                        elif int(new_state)-int(n_state)==-SIZE:
                            action_index=2
                        #down
                        elif int(new_state)-int(n_state)==SIZE:
                            action_index=3

                        self.q_table[int(n_state)][action_index] = self.q_table[int(n_state)][action_index] * (1 - self.learning_rate) + \
                                                            self.learning_rate * (
                                                                    reward + self.discount_rate * np.max(
                                                                self.q_table[int(new_state), :]))+10*SIZE*SIZE
            

                #lose
                
                if FLAG_win==True and answer[2]==0 and answer[3]==0:
                    #print("dead")
                    print(finalanswer)
                    print("length of answer ", len(finalanswer))
                    #break
                if answer[1]==True:
                    maxSteps=len(answer[0])-1
                    FLAG_win=True
                    finalanswer=answer[0]
                
        
            #print(answer)
            #find convergence
            self.bigChange= np.ndarray.max(np.abs(np.subtract(old_q,self.q_table)))
            self.episodes=self.episodes+1
            if self.bigChange<=self.epsilon :
                break
    
    def print_results(self):
        print('big Change')
        print('{:010.10f}'.format(self.bigChange))
        print('Episodes')
        print(self.episodes)
        writeSmv(SIZE, 10000 ,self.q_table, self.env.get_holes())
        answer=runSmv()
                
        if answer[1]==True:
         print("found something ", len(answer[0]))
         print(answer[0])


        print('Q-Table')
        print(self.q_table)
        print('-------------------------------------')

        # Calculate and print the average reward per thousand episodes
        avg_reward=sum(self.all_episode_rewards) / self.episodes

        print("Average reward:")
        print(avg_reward)
        print()

    def run_and_print_latest_iteration(self):
        state = self.env.reset()
        for step in range(self.max_steps_per_episode):
            #self.env.print_current_state()
            #time.sleep(1)
            action_index = np.argmax(self.q_table[state, :])
            new_state, _, done = self.env.step(action_index)
            state = new_state

            if done and state==SIZE*SIZE-1:
                print('The agent has reached the goal!!!')
                return 1
            if done:
              break
        return 0