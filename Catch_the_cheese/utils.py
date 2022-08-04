import os
from pickle import FALSE
import subprocess
import numpy as np
from action import Action
import parameters_run
SIZE=parameters_run.get_size()
import environment
import math

def writeStart(filename):
    if os.path.exists(filename):
        os.remove(filename)  #create new file

    #write beginning of smv file
    with open(filename, 'w') as fw:
        fw.write("MODULE main\n\nVAR\n	currentPosition : ")
        lw = '{'
        for i in range(SIZE):
            lw = lw + str(i) + ', '
        lw = lw[:-2]
        fw.write(lw)
        fw.write("};\n")
        fw.write("	score : ")
        lw = '{'
        for i in range(12):
            lw = lw + str(i) + ', '
        lw = lw[:-2]
        fw.write(lw)
        fw.write("};\n")
        fw.write("\n\nASSIGN")

        fw.write("			\n\n	init(currentPosition) := "+str(parameters_run.get_start_point_model_checker())+ ";")

        #this is the counter 
        fw.write("			\n\n	init(score) := 0;\n\n")

        fw.write("    next(currentPosition) := case\n")

def bestActions(q_line,user_po):
    actionList=[]
    bestactionlist=[]
    
    if legalActions(0,user_po):
     bestactionlist.append(user_po-1)
    if legalActions(1,user_po):
     bestactionlist.append(user_po+1)
    
    return bestactionlist


def legalActions(index,user_po):
    #the actions that are illegal:
    #   can't go up once you are at top of board
    #   can't go down once you are at bottom of board
    #   can't go left or right once you are at edge of board
    
        #left
    if index==0 and user_po%SIZE!=(0):
        return True
        #right
    if index==1 and user_po%SIZE!=(SIZE-1):
        return True
      
    return False

def writePlayer(filename, listOfHoles, currentOptimal, Q):
    if os.path.exists(filename):
        os.remove(filename)
    
    #write rest of smv file
    with open(filename, 'w') as fw:
        for i in range(len(listOfHoles)):
            fw.write(f"               currentPosition = "+ str(listOfHoles[i])+ ": " + "{" + str(listOfHoles[i]) + "};\n")
        fw.write(f"               currentPosition = "+ str(SIZE-1)+"&score<9"+ ": " + "{" + str(SIZE-2) + "};\n")
        fw.write(f"               currentPosition = "+ str(SIZE-1)+ "&score>=10: " + "{" + str(SIZE-1) + "};\n")
        for i in range(SIZE-1):
            if i not in listOfHoles:
                bestMove=bestActions(Q[i],i)
                fw.write(f"               currentPosition = "+ str(i) + ": " + "{")
                lw = ""
                
                for i in range(len(bestMove)):
                    lw = lw + str(bestMove[i]) + ','
                
                #lw = lw + str(bestMove[0]) + ','
                lw = lw[:-1]
                lw = lw + "};\n"
                fw.write(lw)
        fw.write("               TRUE : currentPosition;\n")
        fw.write("    esac;\n\n")
        fw.write("    next(score) := case\n")
        fw.write("               score = score&score<" +str(10) +"&currentPosition="+str(SIZE-1)+" : score+1;\n")
        fw.write("               TRUE : score;\n")
        fw.write("    esac;\n\n")

        #LTL line
        fw.write("LTLSPEC !F (score>=10)\n")
        #fw.write("LTLSPEC F ((currentPosition ="+str(SIZE*SIZE-1)+")&(countSteps<"+str(int(10*SIZE))+"))\n")


# main function of writing the smv file
def writeSmv(SIZE, currentOptimal, Q, listOfHoles):
    filename_main = 'tests/test_t1.smv'
    if os.path.exists(filename_main):
        os.remove(filename_main)
    with open(filename_main, 'w') as fw:
        filename_start = f'tests/add_start_{1}{SIZE}.txt'
        writeStart(filename_start)
        with open(filename_start, 'r') as fr:
            for line in fr:
                fw.write(line)

        filename_player = f'tests/{1}playersnextC{SIZE}.txt'
        writePlayer(filename_player, listOfHoles, currentOptimal, Q)
        with open(filename_player, 'r') as fr:
            for line in fr:
                fw.write(line)


# run smv file and check the result
def runSmv():
    smv_file = f'test_t1.smv'
    os.chdir('tests')
    output = subprocess.check_output(['nuXmv', smv_file], shell=True).splitlines()
    os.chdir('../')
    ans = str(output[26][47:])[2:]
    ans = ans[0:len(ans) - 1]
    moveList=list()
   
    if 'false' in str(output):
        loop_vecs = str(b''.join(output))
        chunks = loop_vecs.split(' ')
        FLAG=False
        for i in range(len(chunks)) :
            if chunks[i] == 'Counterexample':
                FLAG=True
            if chunks[i]== 'currentPosition' and FLAG:
                moveList.append((chunks[i+2]))
        
    return moveList,True,0,0