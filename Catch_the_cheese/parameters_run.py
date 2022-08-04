
size=10
useNusmv=1
num_steps_in_episode=7
start_point=0
score=5
def get_size():
    return size

def get_score():
    return score

def get_useNusmv():
    return useNusmv


def get_num_steps_in_episode():
    return num_steps_in_episode

def get_start_point():
    return start_point

def get_start_point_model_checker():
    return start_point+num_steps_in_episode

def set_use_Nuxmv(value):
    useNusmv=value