# Formal_verification_with_RL
Official implementation of "Learning Through Imitation by using Formal
Verification"



## Introduction
Reinforcement-Learning-based solutions have achieved many
successes in numerous complex tasks. However, their training process has
a tendency to be unstable, and achieving convergence can be difficult,
expensive, and in some instances impossible. We propose herein a novel
approach that enables the integration of strong formal verification meth-
ods in order to improve the learning process as well as prove convergence.
During the learning process, formal methods serve as experts to identify
weaknesses in the learned model, improve it, and even lead it to con-
verge. By evaluating our approach on several common problems, which
have already been studied and solved by classical methods, we demon-
strate the strength and potential of our core idea of incorporating formal
methods into the training process of Reinforcement Learning methods.

## Games
### Cops and robbers:
using the model checker as expert who tells us in which starting points the robbers will get away,and then start the next episod from this point. help us to reach the optimal solution with much less iterations. in order to use the model checker you will need directory tests and put it there with the txt files:add_end.txt,add_LTL.txt,add_CTL.txt run from CaRgame.py


### Frozen lake:
we showed that when RL algorithm Q learning failed to find the optimal solution for the game frozen lake the model checker when used as an expert can help the Q learning learn the optimal solution. To change the size of the board:change the parameter size in parametrs_run.py To activate the model checker change useNusmv to 1 in parametrs_run.py else 0 There need to be a model checker in a directory tests in order to use it.

### Catch the cheese:
in this cide we showed how model checkers can be used as expert and help a RL algorithm learn the optimal move in states he did not see during the training. when we do not give enough steps the algorithm ca not learn the solution but the model checker is able to teach him the right move. change the parameters un the file parameters_run.py. in order to use the model checker there need to be a directory tetst and put the model checker there.

