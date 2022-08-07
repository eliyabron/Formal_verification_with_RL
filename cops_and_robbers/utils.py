import os
import subprocess
import numpy as np
import random
# defines
BOARD_ROWS = 5
BOARD_COLS = BOARD_ROWS
# INIT = [[[3, 2], [2, 2]], [[1, 1]]]
INIT = [[[1, 1], [1, 2]], [[2, 2]]]


# convert init state to vector
def InitToNumbers(ret_type):
    init_vec = str(INIT)
    toRemove = ['[', ']', ' ', ',']
    for t in toRemove:
        init_vec = init_vec.replace(t, '')
    return ret_type(init_vec)


# rotate number by 90
def rotate_num(num):
    i = int(num / 10)
    j = num % 10
    return 10 * (BOARD_ROWS - j) + i


# rotate full vec
def rotate_vec(vec, angle=1):
    sum_rvec = 0
    for loop in range(angle):
        for i in range(int(len(str(vec)) / 2)):
            n = int(str(vec)[2 * i: 2 * i + 2])
            sum_rvec = 100 * sum_rvec + rotate_num(n)
        vec = sum_rvec
        sum_rvec = 0
    return rearrange_vector(vec)


# mirror number
def mirror_num(num, angle='horizontal'):
    i = int(num / 10)
    j = num % 10
    if angle == 'horizontal':
        return 10 * i + (BOARD_ROWS - j)
    elif angle == 'vertical':
        return 10 * (BOARD_ROWS - i) + j


# mirror full vec
def mirror_vec(vec, angle='horizontal'):
    sum_mvec = 0
    for i in range(int(len(str(vec)) / 2)):
        n = int(str(vec)[2 * i: 2 * i + 2])
        sum_mvec = 100 * sum_mvec + mirror_num(n, angle)
    return rearrange_vector(sum_mvec)


# check if vector already exist in any manipulation
def vec_exist(vec, vecs):
    if rotate_vec(vec, 1) in vecs:
        return 1
    if rotate_vec(vec, 2) in vecs:
        return 2
    if rotate_vec(vec, 3) in vecs:
        return 3
    if mirror_vec(vec, 'horizontal') in vecs:
        return 4
    if mirror_vec(rotate_vec(vec, 1), 'horizontal') in vecs:
        return 5
    if mirror_vec(rotate_vec(vec, 2), 'horizontal') in vecs:
        return 6
    if mirror_vec(rotate_vec(vec, 3), 'horizontal') in vecs:
        return 7
    # if mirror_vec(vec, 'vertical') in vecs:
    # return 5
    # need to fix the rest
    return False


# sort vector to avoiding duplicate.
# since 111223 equal to 121123 (because the first 4 digits are 2 cops),
# we sort the place of cops
def rearrange_vector(vec):
    rob_po = vec % 100
    cop_po = int(vec / 100)
    cop_agents = int(len(str(cop_po)) / 2)
    cop_list = []
    for ca in range(cop_agents):
        if ca == 0:
            cop_list.append(int(cop_po % 100))
        else:
            cop_list.append(int(cop_po / (10 ** 2 ** ca) % 100))
    cop_list.sort()
    res_sort = 0
    for ca in cop_list:
        res_sort = 100 * res_sort + ca
    res_ret = 100 * res_sort + rob_po
    return res_ret


# find equal vec in l_vecs
def findEqual(cand, v_vecs):
    if not validVec(cand):
        return 0
    if rotate_vec(cand, 1) in v_vecs:
        return rotate_vec(cand, 1)
    if rotate_vec(cand, 2) in v_vecs:
        return rotate_vec(cand, 2)
    if rotate_vec(cand, 3) in v_vecs:
        return rotate_vec(cand, 3)
    if mirror_vec(cand, 'horizontal') in v_vecs:
        return mirror_vec(cand, 'horizontal')
    if mirror_vec(rotate_vec(cand, 1), 'horizontal') in v_vecs:
        return mirror_vec(rotate_vec(cand, 1), 'horizontal')
    if mirror_vec(rotate_vec(cand, 2), 'horizontal') in v_vecs:
        return mirror_vec(rotate_vec(cand, 2), 'horizontal')
    if mirror_vec(rotate_vec(cand, 3), 'horizontal') in v_vecs:
        return mirror_vec(rotate_vec(cand, 3), 'horizontal')
    return False


# def inerse_findEqual(cand, v_vecs):
#    if rotate_vec(cand, 1) in v_vecs:
#        return rotate_vec(cand, 1)
#    if rotate_vec(cand, 2) in v_vecs:
#        return rotate_vec(cand, 2)
#    if rotate_vec(cand, 3) in v_vecs:
#        return rotate_vec(cand, 3)
#    if mirror_vec(cand, 'horizontal') in v_vecs:
#        return mirror_vec(cand, 'horizontal')
#    if mirror_vec(rotate_vec(cand, 1), 'horizontal') in v_vecs:
#        return mirror_vec(rotate_vec(cand, 1), 'horizontal')
#    if mirror_vec(rotate_vec(cand, 2), 'horizontal') in v_vecs:
#        return mirror_vec(rotate_vec(cand, 2), 'horizontal')
#    if mirror_vec(rotate_vec(cand, 3), 'horizontal') in v_vecs:
#        return mirror_vec(rotate_vec(cand, 3), 'horizontal')
#    return False

# check if any cop sit on same slot of rob
def copWin(cop_sum, rob_po):
    if type(cop_sum) == list:
        cop_sum = str(cop_sum)
        toRemove = ['[', ']', ' ', ',']
        for t in toRemove:
            cop_sum = cop_sum.replace(t, '')
        cop_sum = int(cop_sum)
    cop_l = []
    while True:
        cop_l.append(cop_sum % 100)
        cop_sum = int(cop_sum / 100)
        if cop_sum == 0:
            break
    if rob_po in cop_l:
        return True
    else:
        return False


# convert index to digit
def index_to_number(vec):
    vec_ul = sum(vec, [])
    res_itn = 0  # itn is Index To Number
    for i in range(len(vec_ul)):
        res_itn = res_itn + vec_ul[i] * (10 ** (len(vec_ul) - i - 1))
    return res_itn


# find the all options for the next turn
def next_positions(pl_turn, list_of_position, max_digit=10):
    cop_po = list_of_position[0]
    rob_po = list_of_position[1]
    res_po = []
    if pl_turn == 1:  # cop turn
        for cp in cop_po:
            i = cp[0]
            j = cp[1]
            if i > 1 and [i - 1, j] not in cop_po:
                if len(cop_po) == 1:
                    res_po.append([[[i - 1, j]]])
                else:
                    res_po.append([[[i - 1, j]], [p for p in cop_po if p != cp][:]])
            if j > 1 and [i, j - 1] not in cop_po:
                if len(cop_po) == 1:
                    res_po.append([[[i, j - 1]]])
                else:
                    res_po.append([[[i, j - 1]], [p for p in cop_po if p != cp][:]])
            if i + 1 != BOARD_ROWS and i + 1 <= max_digit and [i + 1, j] not in cop_po:
                if len(cop_po) == 1:
                    res_po.append([[[i + 1, j]]])
                else:
                    res_po.append([[[i + 1, j]], [p for p in cop_po if p != cp][:]])
            if j + 1 != BOARD_COLS and j + 1 <= max_digit and [i, j + 1] not in cop_po:
                if len(cop_po) == 1:
                    res_po.append([[[i, j + 1]]])
                else:
                    res_po.append([[[i, j + 1]], [p for p in cop_po if p != cp][:]])
    else:
        i = rob_po[0][0]
        j = rob_po[0][1]
        if i > 1 and [i - 1, j] not in cop_po:
            res_po.append([i - 1, j])
        if j > 1 and [i, j - 1] not in cop_po:
            res_po.append([i, j - 1])
        if i + 1 != BOARD_ROWS and i + 1 <= max_digit and [i + 1, j] not in cop_po:
            res_po.append([i + 1, j])
        if j + 1 != BOARD_COLS and j + 1 <= max_digit and [i, j + 1] not in cop_po:
            res_po.append([i, j + 1])
    if not res_po:
        return None
    return res_po


# check if vector is valid:
# not contain 0
# not contain number that grater than the grid
# every player on different slot
def validVec(vec, max_digit=9):
    for d in str(vec):
        if int(d) > max_digit or int(d) == 0:
            return False
    rob_po = vec % 100
    cop_po = int(vec / 100)
    cop_agents = int(len(str(cop_po)) / 2)
    all_list = []
    for ca in range(cop_agents):
        if ca == 0:
            all_list.append(int(cop_po % 100))
        else:
            all_list.append(int((cop_po / (10 ** 2 ** ca) % 100)))
    all_list.append(rob_po)
    if not all(element > 10 and element % 10 != 0 for (element) in all_list):
        return False
    if len(all_list) != len(set(all_list)):
        return False
    return True


# Generate 2 lists: 1. a list with all valid vecs. 2. A short list, containing one representation of each state
def createVecs(numOfPlayers, max_grid=9):
    full_vecs = [0]
    vecs = [0]
    path = f"tests/vecs{numOfPlayers}{max_grid}.txt"
    if os.path.exists(path):
        with open(path, 'r') as fr:
            vecs = fr.read()[1:-1]
            vecs = list(vecs.split(", "))
            vecs = list(map(int, vecs))
    else:
        for i in range(10 ** (2 * numOfPlayers - 1), int(10 ** (2 * numOfPlayers) * ((max_grid + 1) / 10)), 1):
            if i != rearrange_vector(i):
                continue
            if i not in vecs:
                if validVec(i, max_grid):
                    full_vecs.append(i)
        for vf in full_vecs:
            if not bool(vec_exist(vf, vecs)):
                vecs.append(vf)
    return full_vecs, vecs


# write the first part of smv file
def writeStart(l_v, filename):
    if os.path.exists(filename):
        os.remove(filename)  # return
    with open(filename, 'w') as fw:
        fw.write("MODULE main\n\nVAR\n	vec : ")
        lw = '{0, '
        for av in l_v:
            if av == 0:
                continue
            lw = lw + 'v' + str(av) + ', '
        lw = lw[:-2]
        fw.write(lw)
        fw.write("};\n")
        fw.write("	player : {C, R};\n	-- 0 = COP WIN, 5 = ROB WIN\n\nASSIGN\n\n")
        fw.write("	init(player) := C;\n")
        fw.write("	next(player) := case\n				player = R: C;\n				player = C: R;\n")
        fw.write("			esac;\n\n	init(vec) := ")

        init_vec = '{0, '
        for lv in l_v:
            if lv == 0:
                continue
            init_vec = init_vec + 'v' + str(lv) + ', '
        init_vec = init_vec[:-2]
        fw.write(init_vec)
        fw.write("};\n\n    next(vec) := case\n")


# write cops part of smv file
def writeCop(p1, l_vecs, max_digit, filename):
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, 'w') as fw:
        for s in l_vecs:
            if s == 0:
                continue
            swpos = str(s)
            wpos = [[], []]
            for lw in range(int(len(swpos[:-2]) / 2)):
                wpos[0].append([int(swpos[2 * lw]), int(swpos[2 * lw + 1])])
            wpos[1].append([int(swpos[-2]), int(swpos[-1])])
            nextwv = next_positions(1, wpos, max_digit)
            l_next = []
            l_next_val = []
            rob_po = int(s % 100)
            for li in nextwv:
                li = sum(sum(li, []), [])
                cop_sum = 0
                for i in range(len(li)):
                    i = i + 1
                    cop_sum = cop_sum + 10 ** (i + 1) * li[-i]
                l_append = rearrange_vector(cop_sum + rob_po)
                if l_append not in l_vecs:
                    l_append = findEqual(l_append, l_vecs)
                l_next_val.append('v' + str(l_append))
                if copWin(int(cop_sum / 100), rob_po):
                    if '0' not in l_next:
                        l_next.append(str(0))
                else:
                    if l_append not in l_vecs:
                        l_append = findEqual(l_append, l_vecs)
                    l_next.append('v' + str(l_append))
            if l_next != '0':
                l_next = ', '.join(l_next)
                l_next_val = ', '.join(l_next_val)
            l_next_max = l_next_val.replace('v', '')
            l_next_max = l_next_max.split(', ')
            list_next_int = list(map(int, l_next_max))
            list_states_int = list(p1.states_value.keys())
            if bool(sum(map(lambda x: x in list_next_int, list_states_int))):
                max_value = -999
                for i in l_next_max:
                    i = int(i)
                    val = p1.states_value.get(i)
                    if val:
                        if p1.states_value.get(i) >= max_value:
                            max_value = p1.states_value[i]
                            if i != 0:
                                l_next_max_ret = 'v' + str(i)
                            else:
                                l_next_max_ret = 0
                l_next = l_next_max_ret
                # l_next_temp = [int(x) for x in str(l_next[1:])]
                # cop_list = int(int(''.join(str(i) for i in l_next_temp)) / 100)
                # if copWin(cop_list, l_next_temp[-2] * 10 + l_next_temp[-1]):
                #     l_next = '0'
            fw.write(f"                player = C & vec = v{s} : " + "{" + f"{l_next}" + "};\n")


# write rob part of smv file
def writeRob(vecs, max_digit, filename):
    if os.path.exists(filename):
        os.remove(filename)  # return
    with open(filename, 'w') as f:
        for wv in vecs:
            if wv == 0:
                continue
            swpos = str(wv)
            wpos = [[], []]
            for lw in range(int(len(swpos[:-2]) / 2)):
                wpos[0].append([int(swpos[2 * lw]), int(swpos[2 * lw + 1])])
            wpos[1].append([int(swpos[-2]), int(swpos[-1])])
            nextwv = next_positions(-1, wpos, max_digit)
            if nextwv is None:
                nextwv = [[int((wv % 100) / 10), wv % 10]]
            l_next = []
            cop_po = int(wv / 100)
            for li in nextwv:
                cand = cop_po * 100 + li[0] * 10 + li[1]
                if cand not in vecs:
                    cand = findEqual(cand, vecs)
                l_next.append('v' + str(cand))
            l_next = ', '.join(l_next)
            f.write(f"                player = R & vec = v{wv} : " + "{" + f"{l_next}" + "};\n")


# main function of writing the smv file
def writeSmv(numOfPlayers, max_digit, p1, all_vecs, l_vecs):
    filename_main = 'tests/test_t3.smv'
    if os.path.exists(filename_main):
        os.remove(filename_main)
    with open(filename_main, 'w') as fw:
        filename_start = f'tests/add_start_{numOfPlayers}{max_digit}.txt'
        writeStart(l_vecs, filename_start)
        with open(filename_start, 'r') as fr:
            for line in fr:
                fw.write(line)

        filename_rob = f'tests/{numOfPlayers}playersnextR{max_digit}.txt'
        writeRob(l_vecs, max_digit, filename_rob)
        with open(filename_rob, 'r') as fr:
            for line in fr:
                fw.write(line)

        filename_cop = f'tests/{numOfPlayers}playersnextC{max_digit}.txt'
        writeCop(p1, l_vecs, max_digit, filename_cop)
        with open(filename_cop, 'r') as fr:
            for line in fr:
                fw.write(line)

        with open('tests/add_end.txt', 'r') as fr:
            for line in fr:
                fw.write(line)

    #print("done!")


# run smv file and check the result
def runSmv():
    smv_file = f'test_t3.smv'
    os.chdir('tests')
    output = subprocess.check_output(['nuXmv', smv_file], shell=True).splitlines()
    os.chdir('../')
    ans = str(output[26][47:])[2:]
    ans = ans[0:len(ans) - 1]
    if ans == 'true':
        return 'win', True
    else:
        loop_vecs = str(b''.join(output))
        loop_vecs = loop_vecs[loop_vecs.find("State"):]
        if loop_vecs.find('R') < loop_vecs.find('C'):
            loop_vecs = loop_vecs[loop_vecs.find('R'):]
        flag = True
        wordList = loop_vecs.split()
        wl_c = []
        wl_r = []
        for wl in wordList:
            if wl[0] == 'v' and len(wl) == (1 + len(InitToNumbers(str))):
                if flag:
                    wl_c.append(wl)
                else:
                    wl_r.append(wl)
                flag = not flag
        wl_c = ' '.join(wl_c).replace('v', '').split()
        wl_r = ' '.join(wl_r).replace('v', '').split()
        idx = np.random.choice(len(wl_c))
        init = wl_c[idx]
        return int(init), int(wl_r[0])

# write the first part of smv file
def writeStart1(l_v, filename):
    if os.path.exists(filename):
        os.remove(filename)  # return
    with open(filename, 'w') as fw:
        fw.write("MODULE main\n\nVAR\n	vec : ")
        lw = '{0, '
        for av in l_v:
            if av == 0:
                continue
            lw = lw + 'v' + str(av) + ', '
        lw = lw[:-2]
        fw.write(lw)
        fw.write("};\n")
        fw.write("	player : {C, R};\n	-- 0 = COP WIN, 5 = ROB WIN\n\nASSIGN\n\n")
        fw.write("	init(player) := C;\n")
        fw.write("	next(player) := case\n				player = R: C;\n				player = C: R;\n")
        fw.write("			esac;\n\n	init(vec) := ")

        init_vec = '{'
        lv=0
        while lv==0:
         lv=random.choice(l_v)
        if lv!=0:
         init_vec = init_vec + 'v' + str(lv) + ', '
        init_vec = init_vec[:-2]
        fw.write(init_vec)
        fw.write("};\n\n    next(vec) := case\n")


# write cops part of smv file
def writeCop1(p1, l_vecs, max_digit, filename):
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, 'w') as fw:
        for s in l_vecs:
            if s == 0:
                continue
            swpos = str(s)
            wpos = [[], []]
            for lw in range(int(len(swpos[:-2]) / 2)):
                wpos[0].append([int(swpos[2 * lw]), int(swpos[2 * lw + 1])])
            wpos[1].append([int(swpos[-2]), int(swpos[-1])])
            nextwv = next_positions(1, wpos, max_digit)
            l_next = []
            l_next_val = []
            rob_po = int(s % 100)
            for li in nextwv:
                li = sum(sum(li, []), [])
                cop_sum = 0
                for i in range(len(li)):
                    i = i + 1
                    cop_sum = cop_sum + 10 ** (i + 1) * li[-i]
                l_append = rearrange_vector(cop_sum + rob_po)
                if l_append not in l_vecs:
                    l_append = findEqual(l_append, l_vecs)
                l_next_val.append('v' + str(l_append))
                if copWin(int(cop_sum / 100), rob_po):
                    if '0' not in l_next:
                        l_next.append(str(0))
                else:
                    if l_append not in l_vecs:
                        l_append = findEqual(l_append, l_vecs)
                    l_next.append('v' + str(l_append))
            if l_next != '0':
                l_next = ', '.join(l_next)
                l_next_val = ', '.join(l_next_val)
            l_next_max = l_next_val.replace('v', '')
            l_next_max = l_next_max.split(', ')
            list_next_int = list(map(int, l_next_max))
            list_states_int = list(p1.states_value.keys())
            if bool(sum(map(lambda x: x in list_next_int, list_states_int))):
                max_value = -999
                for i in l_next_max:
                    i = int(i)
                    val = p1.states_value.get(i)
                    if val:
                        if p1.states_value.get(i) >= max_value:
                            max_value = p1.states_value[i]
                            if i != 0:
                                l_next_max_ret = 'v' + str(i)
                            else:
                                l_next_max_ret = 0
                l_next = l_next_max_ret
                # l_next_temp = [int(x) for x in str(l_next[1:])]
                # cop_list = int(int(''.join(str(i) for i in l_next_temp)) / 100)
                # if copWin(cop_list, l_next_temp[-2] * 10 + l_next_temp[-1]):
                #     l_next = '0'
            fw.write(f"                player = C & vec = v{s} : " + "{" + f"{l_next}" + "};\n")


# write rob part of smv file
def writeRob1(vecs, max_digit, filename):
    if os.path.exists(filename):
        os.remove(filename)  # return
    with open(filename, 'w') as f:
        for wv in vecs:
            if wv == 0:
                continue
            swpos = str(wv)
            wpos = [[], []]
            for lw in range(int(len(swpos[:-2]) / 2)):
                wpos[0].append([int(swpos[2 * lw]), int(swpos[2 * lw + 1])])
            wpos[1].append([int(swpos[-2]), int(swpos[-1])])
            nextwv = next_positions(-1, wpos, max_digit)
            if nextwv is None:
                nextwv = [[int((wv % 100) / 10), wv % 10]]
            l_next = []
            cop_po = int(wv / 100)
            for li in nextwv:
                cand = cop_po * 100 + li[0] * 10 + li[1]
                if cand not in vecs:
                    cand = findEqual(cand, vecs)
                l_next.append('v' + str(cand))
            l_next = ', '.join(l_next)
            f.write(f"                player = R & vec = v{wv} : " + "{" + f"{l_next}" + "};\n")


# main function of writing the smv file
def writeSmv1(numOfPlayers, max_digit, p1, all_vecs, l_vecs):
    filename_main = 'tests/test_t3.smv'
    if os.path.exists(filename_main):
        os.remove(filename_main)
    with open(filename_main, 'w') as fw:
        filename_start = f'tests/add_start_{numOfPlayers}{max_digit}.txt'
        writeStart1(l_vecs, filename_start)
        with open(filename_start, 'r') as fr:
            for line in fr:
                fw.write(line)

        filename_rob = f'tests/{numOfPlayers}playersnextR{max_digit}.txt'
        writeRob1(l_vecs, max_digit, filename_rob)
        with open(filename_rob, 'r') as fr:
            for line in fr:
                fw.write(line)

        filename_cop = f'tests/{numOfPlayers}playersnextC{max_digit}.txt'
        writeCop1(p1, l_vecs, max_digit, filename_cop)
        with open(filename_cop, 'r') as fr:
            for line in fr:
                fw.write(line)

        with open('tests/add_end_LTL.txt', 'r') as fr:
            for line in fr:
                fw.write(line)

    #print("done!")


# run smv file and check the result
def runSmv1():
    smv_file = f'test_t3.smv'
    os.chdir('tests')
    output = subprocess.check_output(['nuXmv', smv_file], shell=True).splitlines()
    os.chdir('../')
    ans = str(output[26][47:])[2:]
    ans = ans[0:len(ans) - 1]
    if ans == 'true':
        return 'win', True
    else:
        loop_vecs = str(b''.join(output))
        loop_vecs = loop_vecs[loop_vecs.find("State"):]
        if loop_vecs.find('R') < loop_vecs.find('C'):
            loop_vecs = loop_vecs[loop_vecs.find('R'):]
        flag = True
        wordList = loop_vecs.split()
        wl_c = []
        wl_r = []
        for wl in wordList:
            if wl[0] == 'v' and len(wl) == (1 + len(InitToNumbers(str))):
                if flag:
                    wl_c.append(wl)
                else:
                    wl_r.append(wl)
                flag = not flag
        wl_c = ' '.join(wl_c).replace('v', '').split()
        wl_r = ' '.join(wl_r).replace('v', '').split()
        #print(wl_c)
        #idx = np.random.choice(len(wl_c))   # we choose randomly state from the list of states
                                            # the cop passed on last ruuning
        #init = wl_c[idx] 
        wl_c = [int(i) for i in wl_c]                   #  the chosen state use as start position for next game
        return wl_c, wl_r    # the rob initial position stay the same




# if __name__ == "__main__":
#     a, v = createVecs(3, 4)
#     vec_sim = 113221
#     sim = rotate_vec(vec_sim, 1)
#     print(sim)
