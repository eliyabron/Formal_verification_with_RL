# Formal verification with RL
Official implementation of "Learning Through Imitation by using Formal
Verification"

![](https://github.com/eliyabron/Formal_verification_with_RL/blob/main/Images/Fig1.jpg)

## Introduction
<p align="justify">
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
</p>

## Installation and run steps:
<p align="justify">

1.	First Download and Install nuXmv from [this link](https://nuxmv.fbk.eu/pmwiki.php?n=Download.Download).

2.	Create a folder in which to save the desired code.

3.	Open a new folder named “tests” and put a copy of nuXmv in there.

4. In each game run the code from the file:

   * Cops and Robbers: CaRgame_1.py
   
   * Frozen Lake: main.py
   
   * Catch the Cheese: main.py
</p>

## Games

![](https://github.com/eliyabron/Formal_verification_with_RL/blob/main/Images/Games.jpg)

### Cops and robbers:
<p align="justify">
Using the model checker as expert who tells us in which starting points the robbers will get away, and then start the next episod from this point. Help us to reach the optimal solution with much less iterations. Save the following files in test directory: add_end.txt, add_LTL.txt ,add_CTL.txt, and run the following script:
</p>

```
CaRgame.py
```


### Frozen lake:
<p align="justify">
We showed that when RL algorithm Q-learning failed to find the optimal solution for the game frozen lake the model checker when used as an expert can help the Q-learning learn the optimal solution. One can control the size of the board by change the parameter size in parametrs_run.py. To activate the model checker change useNusmv to 1 in the same script.
</p>

![](https://github.com/eliyabron/Formal_verification_with_RL/blob/main/Images/Hard.jpg)

### Catch the cheese:
<p align="justify">
In this case we showed how model checkers can be used as expert and help a RL algorithm learn the optimal move in states he did not see during the training. When we do not give enough steps the algorithm cannot learn the solution but the model checker is able to teach him the right move. Change the parameters in the file parameters_run.py.
</p>
