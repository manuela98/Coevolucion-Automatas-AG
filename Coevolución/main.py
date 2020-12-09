import numpy as np
import yaml
from tqdm import tqdm

from components import Robot, robot_from_dna, Coevolution

# import settings
with open("config.yaml", "r") as yamlfile:
    config = yaml.safe_load(yamlfile)

pop_size = config['pop_size'] # number of robots per generation
num_breeders = config['num_breeders'] # number of robots who can mate in each generation
num_gen = config['num_generations'] # total number of generations
iter_per_sim = config['iterations_per_simulation'] # number of rubbish-collection simulations per robot
moves_per_iter = config['moves_per_iteration'] # number of moves robot can make per simulation


# initial population
pop_one = [Robot() for x in range(pop_size)]
pop_two = [Robot() for x in range(pop_size)]
results_one = []
results_two = []
results_system = []

# run evolution
for i in tqdm(range(num_gen)):
    scores_one = np.zeros(pop_size)
    scores_two = np.zeros(pop_size)
    scores_system = np.zeros(pop_size)
    # iterate through all robots
    for idx in range(len(pop_one)):
    # run rubbish collection simulation and calculate fitness
        coevolution = Coevolution(pop_one[idx],pop_two[idx])
        score_one,score_two,system = coevolution.simulate(iter_per_sim, moves_per_iter)
        scores_one[idx] = score_one
        scores_two[idx] = score_two
        scores_system[idx] = system
  
    results_one.append([scores_one.mean(),scores_one.max()]) # save mean and max scores for each generation
    results_two.append([scores_two.mean(),scores_two.max()]) # save mean and max scores for each generation
    results_system.append([scores_system.mean(),scores_system.max()]) # save mean and max scores for each generation
    print(scores_one.max(),scores_two.max())
    best_robot_one = pop_one[scores_one.argmax()] # save the best robot
    best_robot_two = pop_two[scores_two.argmax()] # save the best robot

    # limit robots who are able to mate to top num_breeders
    inds_one = np.argpartition(scores_one, -num_breeders)[-num_breeders:] # get indices of top robots based on fitness
    inds_two = np.argpartition(scores_two, -num_breeders)[-num_breeders:] # get indices of top robots based on fitness
    subpop_one = []
    subpop_two = []
    for i in range(len(inds_one)):
        subpop_one.append(pop_one[inds_one[i]])
        subpop_two.append(pop_two[inds_two[i]])
        
    scores_one = scores_one[inds_one]
    scores_two = scores_two[inds_two]

    # square and normalise fitness scores
    norm_scores_one = (scores_one - scores_one.min()) ** 2
    norm_scores_one = norm_scores_one / norm_scores_one.sum()

    norm_scores_two = (scores_two - scores_two.min()) ** 2
    norm_scores_two = norm_scores_two / norm_scores_two.sum()

    # create next generation of robots
    new_pop_one = []
    new_pop_two = []
    for child in range(pop_size):
        p1, p2 = np.random.choice(subpop_one, p=norm_scores_one, size=2, replace=False)
        p3, p4 = np.random.choice(subpop_two, p=norm_scores_two, size=2, replace=False)
        new_pop_one.append(Robot(p1.dna, p2.dna))
        new_pop_two.append(Robot(p3.dna, p4.dna))

    pop_one = new_pop_one
    pop_two = new_pop_two
file = open('output_6.txt','a')
file.write(str(results_one)+'\n')
file.write(str(results_two)+'\n')
file.write(str(results_system)+'\n')
file.write(str(best_robot_one.dna)+'\n')
file.write(str(best_robot_two.dna)+'\n')
coevolution =  Coevolution(best_robot_one,best_robot_two)
coevolution.simulate(1,300,debug=True)
file.write(str(best_robot_one.score)+'\n')
file.write(str(best_robot_two.score)+'\n')
file.close()

