import numpy as np
import yaml

# import settings
with open("config.yaml", "r") as yamlfile:
    config = yaml.safe_load(yamlfile)

rubbish_prob = config['rubbish_probability'] # probability of rubbish in each grid square
grid_size = config['grid_size'] # size of grid (excluding walls)
wall_penalty = config['wall_penalty'] # fitness points deducted for crashing into wall
no_rub_penalty = config['no_rub_penalty'] # fitness points deducted for trying to pickup rubbish in empty square
rubbish_score = config['rubbish_score'] # fitness points awarded for picking up rubbish
mutation_rate = config['mutation_rate'] # probability of a gene mutating
no_your_can_robot_one  = config['not_your_can_robot_A'] # penalty for pick up a can that is not yours
they_collide_robot_one = config['they_collide_robot_A']
no_your_can_robot_two  = config['not_your_can_robot_B'] # penalty for pick up a can that is not yours
they_collide_robot_two = config['they_collide_robot_B']
system_robot_one = config['system_robot_A']
system_robot_two = config['system_robot_B']

class Environment:
    """
    Class for representing a grid environment full of rubbish. Each cell can be:
    'o': empty
    'x': rubbish
    'w': wall
    '*': can other robot
    """
    def __init__(self, p=rubbish_prob, g_size=grid_size):
        self.p = p # probability of a cell being rubbish
        self.g_size = g_size # excluding walls

        # initialise grid and randomly allocate rubbish
        self.grid = np.random.choice(['o','x','*'], size=(self.g_size+2,self.g_size+2), p=(1 - 2*self.p, self.p,self.p))
     
        # set exterior squares to be walls
        self.grid[:,[0,self.g_size+1]] = 'w'
        self.grid[[0,self.g_size+1], :] = 'w'

    def show_grid(self):
        # print the grid in current state
        print(self.grid)

    def remove_rubbish(self,i,j,robot):
        # remove rubbish from specified cell (i,j)
        if robot == 'one':
            # must pick up the x
            if self.grid[i,j] == 'o': # cell already empty
                return 'vacio'

            elif self.grid[i,j] == '*': # cell with other can
                return 'equivocado'
            else:
                self.grid[i,j] = 'o'
                return 'recogio'
            
        if robot == 'two':
            # must pick up the *
            if self.grid[i,j] == 'o': # cell already empty
                return 'vacio'

            elif self.grid[i,j] == 'x': # cell with other can
                return 'equivocado'
            else:
                self.grid[i,j] = 'o'
                return 'recogio'
            

    def get_pos_string(self,i,j):
        # return a string representing the cells "visible" to a robot in cell (i,j)
        return self.grid[i-1,j] + self.grid[i,j+1] + self.grid[i+1,j] + self.grid[i,j-1] + self.grid[i,j]

class Robot:
    """
    Class for representing a rubbish-collecting robot
    """
    def __init__(self, p1_dna=None, p2_dna=None, m_rate=mutation_rate, w_pen=wall_penalty, nr_pen=no_rub_penalty, r_score=rubbish_score):
        self.m_rate = m_rate # mutation rate
        self.wall_penalty = w_pen # penalty for crashing into a wall
        self.no_rub_penalty = nr_pen # penalty for picking up rubbish in empty cell
        self.rubbish_score = r_score # reward for picking up rubbish
        self.p1_dna = p1_dna # parent 1 DNA
        self.p2_dna = p2_dna # parent 2 DNA

        # generate dict to lookup gene index from situation string
        con = ['w','o','x','*'] # wall, empty, rubbish
        self.situ_dict = dict()
        count = 0
        for up in con:
            for right in con:
                for down in con:
                    for left in con:
                        for pos in con:
                            self.situ_dict[up+right+down+left+pos] = count
                            count += 1
        # initialise dna
        self.get_dna()
        
        # positions in each iteration 
        self.i = 0
        self.j = 0
        self.score = 0
    def get_dna(self):
        # initialise dna string for robot
        if self.p1_dna is None:
            # when no parents (first gen) initialise to random string
            self.dna = ''.join([str(x) for x in np.random.randint(7,size=1024)])
        else:
            self.dna = self.mix_dna()

    def mix_dna(self):
        # generate robot dna from parents
        mix_dna = ''.join([np.random.choice([self.p1_dna,self.p2_dna])[i] for i in range(1024)])

        #add mutations
        for i in range(1024):
            if np.random.rand() > 1 - self.m_rate:
                mix_dna = mix_dna[:i] + str(np.random.randint(7)) + mix_dna[i+1:]

        return mix_dna
    
            
class Coevolution:
    
    def __init__(self, robot_one, robot_two, w_pen=wall_penalty, nr_pen=no_rub_penalty, r_score=rubbish_score,they_collide_one =they_collide_robot_one , they_collide_two=they_collide_robot_two ,penalty_can_one=no_your_can_robot_one, penalty_can_two=no_your_can_robot_two, st_one = system_robot_one, st_two=system_robot_two ):
        self.robot_one = robot_one
        self.robot_two = robot_two 
        self.wall_penalty = w_pen
        self.no_rub_penalty = nr_pen
        self.rubbish_score = r_score
        self.they_collide_robot_one = they_collide_one
        self.penalty_can_robot_one = penalty_can_one
        self.they_collide_robot_two = they_collide_two
        self.penalty_can_robot_two = penalty_can_two
        self.system_robot_one = st_one 
        self.system_robot_two = st_two
    
     
    def simulate(self, n_iterations, n_moves, debug=False):
       # simulate rubbish collection
        tot_score_robot_one = 0
        tot_score_robot_two = 0
        for it in range(n_iterations):
            self.robot_one.score= 0 # fitness score
            self.robot_two.score = 0 # fitness score
            self.envir = Environment()
            self.robot_one.i, self.robot_one.j = np.random.randint(1,self.envir.g_size+1, size=2) # randomly allocate starting position
            self.robot_two.i, self.robot_two.j = np.random.randint(1,self.envir.g_size+1, size=2) # randomly allocate starting position
            
            if debug:
                print('before')
                print('start position robot one:',self.robot_one.i, self.robot_one.j)
                print('start position robot one:',self.robot_two.i, self.robot_two.j)
                self.envir.show_grid()
            for move in range(n_moves):
                self.act()
                # if they collide 
                if self.robot_one.i==self.robot_two.i and self.robot_one.j==self.robot_two.j:
                    self.robot_one.score +=  self.they_collide_robot_one
                    self.robot_two.score +=  self.they_collide_robot_two               
            tot_score_robot_one += self.robot_one.score
            tot_score_robot_two += self.robot_two.score
            if debug:
                print('after')
                print('end position robot one:',self.robot_one.i, self.robot_one.j)
                print('end position robot two:',self.robot_two.i, self.robot_two.j)
                self.envir.show_grid()
                print('score robot one:',self.robot_one.score)
                print('score robot two:',self.robot_two.score)
        score_final_one =  tot_score_robot_one / n_iterations
        score_final_two = tot_score_robot_two / n_iterations
        system_score =  score_final_one + score_final_two
        score_final_one_system = score_final_one + self.system_robot_one* system_score
        score_final_two_system = score_final_two + self.system_robot_two* system_score
        return score_final_one_system, score_final_two_system, system_score   # average fitness score across n iterations,  
    
    def act(self):
        # perform action based on DNA and robot situation
        post_str_robot_one = self.envir.get_pos_string(self.robot_one.i, self.robot_one.j) # robot's current situation
        post_str_robot_two = self.envir.get_pos_string(self.robot_two.i, self.robot_two.j) # robot's current situation
        gene_idx_robot_one = self.robot_one.situ_dict[post_str_robot_one] # relevant idx of DNA for current situation
        gene_idx_robot_two = self.robot_two.situ_dict[post_str_robot_two] # relevant idx of DNA for current situation
        act_key_one = self.robot_one.dna[gene_idx_robot_one] # read action from idx of DNA
        act_key_two = self.robot_two.dna[gene_idx_robot_two] # read action from idx of DNA
        
        if act_key_one == '5':
            # move randomly
            act_key_one = np.random.choice(['0','1','2','3'])
        if act_key_two == '5':
            # move randomly
            act_key_two = np.random.choice(['0','1','2','3'])

        if act_key_one == '0':
            self.mv_up('one')
        elif act_key_one == '1':
            self.mv_right('one')
        elif act_key_one == '2':
            self.mv_down('one')
        elif act_key_one == '3':
            self.mv_left('one')
        elif act_key_one == '6':
            self.pickup('one')
            
            
        if act_key_two == '0':
            self.mv_up('two')
        elif act_key_two == '1':
            self.mv_right('two')
        elif act_key_two == '2':
            self.mv_down('two')
        elif act_key_two == '3':
            self.mv_left('two')
        elif act_key_two == '6':
            self.pickup('two')
            
           
        

    def mv_up(self,robot):
        # move up one square
        if robot == 'one':
            if self.robot_one.i == 1:
                self.robot_one.score += self.wall_penalty
            else:
                self.robot_one.i -= 1
        if robot == 'two':
            if self.robot_two.i == 1:
                self.robot_two.score += self.wall_penalty
            else:
                self.robot_two.i -= 1

    def mv_right(self,robot):
        if robot =='one':
            # move right one square
            if self.robot_one.j == self.envir.g_size:
                self.robot_one.score += self.wall_penalty
            else:
                self.robot_one.j += 1
        if robot =='two':
            # move right one square
            if self.robot_two.j == self.envir.g_size:
                self.robot_two.score += self.wall_penalty
            else:
                self.robot_two.j += 1

    def mv_down(self,robot):
        # move down one square
        if robot=='one':
            if self.robot_one.i == self.envir.g_size:
                self.robot_one.score += self.wall_penalty
            else:
                self.robot_one.i += 1
        if robot=='two':
            if self.robot_two.i == self.envir.g_size:
                self.robot_two.score += self.wall_penalty
            else:
                self.robot_two.i += 1


    def mv_left(self,robot):
        if robot=='one':
            # move left one square
            if self.robot_one.j == 1:
                self.robot_one.score += self.wall_penalty
            else:
                self.robot_one.j -= 1
        if robot=='two':
            # move left one square
            if self.robot_two.j == 1:
                self.robot_two.score += self.wall_penalty
            else:
                self.robot_two.j -= 1

    def pickup(self,robot):
        # pickup rubbish
        if robot == 'one':
            success = self.envir.remove_rubbish(self.robot_one.i, self.robot_one.j,robot)
            if success=='recogio':
                # rubbish successfully picked up
                self.robot_one.score += self.rubbish_score
                
            elif success =='equivocado':
                # pick up the another can
                self.robot_one.score += self.penalty_can_robot_one
            else:
                # no rubbish in current square
                self.robot_one.score += self.no_rub_penalty
        if robot == 'two':
            success = self.envir.remove_rubbish(self.robot_two.i, self.robot_two.j,robot)
            if success=='recogio':
                # rubbish successfully picked up
                self.robot_two.score += self.rubbish_score
            elif success =='equivocado':
                # pick up the another can
                self.robot_two.score +=  self.penalty_can_robot_two
            else:
                # no rubbish in current square
                self.robot_two.score += self.no_rub_penalty
    

def robot_from_dna(dna):
    return Robot(p1_dna=dna, p2_dna=dna, m_rate=0)

