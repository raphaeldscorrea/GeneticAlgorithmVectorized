# Genetic Algorithm More Efficient - GAME

```

   ├─── README.md          <- The top-level README for developers using this project.
   │
   ├─── src                <- Source folder containing GAME's funtions and heuristics
   │     │
   │     ├── heuristics              <- Defining SA and GA heuristics          
   │     │    │
   │     │    ├── game                    <- Scripts for Genetic Algorithm approach.
   │     │    │    │
   │     │    │    ├── ga.py                   <- GA's main function.
   │     │    │    │
   │     │    │    ├── nsga_II.py               <- Class to build the NSGA II (Non Dominated Sorting Genetic Algoritm II)
   │     │    │    │
   │     │    │    ├── pareto.py               <- Class that returns the number of desired solutions based on first pareto fronts
   │     │    │    │
   │     │    │    └── operators               <- Scripts for Genetic Algorithm operators.
   │     │    │        │
   │     │    │        ├── binary                      <- Defining binary operators 
   │     │    │        │   ├── crossover.py      
   │     │    │        │   └── mutation.py      
   │     │    │        │
   │     │    │        ├── general                     <- Defining mating and survivor operators
   │     │    │        │   ├── mating.py   
   │     │    │        │   └── suvivor.py  
   │     │    │        │
   │     │    │        └── perm                        <- Defining permutation operators
   │     │    │            ├── crossover.py      
   │     │    │            └── mutation.py         
   │     │    │
   │     │    └── simulated_annealing    <- Scripts for Simulated Annealing approach.
   │     │         │
   │     │         ├── simulated_annealing.py 
   │     │         │
   │     │         └── simulated_annealing_II.py  
   │     │
   │     │    
   │     ├── functions    <- User functions implementations.
   │     │      │
   │     │      ├── decorators.py         <- Decorators to GAME methods
   │     │      │
   │     │      └── objective_function.py <- Objective function (to be updated for each project and for each objective in the case of multiple).
   │     │
   │     │
   │     └── parameters_tuning    <- Racing strategy implementation to find best SA and GA parameters
   │            │
   │            ├── iRace.py 
   │            ├── main.py 
   │            ├── instanceGenerator.py 
   │            ├── configuration.py      
   │            ├── handleraws.py
   │            ├── configuration.py      
   │            ├── preTuning.py   
   │            ├── gaParameters.py
   │            ├── saParameters.py      
   │            └── parallelControl.py 
   │
   ├─── dev
   │     │
   │     └── main.py <- GAME's test functions for developers.
   │     
   └─── tests
         │
         ├── instance.py                        <- Standard instance format for getting inputs and outputs in unit tests
         ├── crossover_test.py                  <- Unitary tests for crossover operators
         ├── mating_test.py                     <- Unitary tests for mating operators
         ├── mutation_test.py                   <- Unitary tests for mutation operators
         ├── survivor_test.py                   <- Unitary tests for survivor operators
         ├── nsga_II_test.py                    <- Unitary tests for nsga_II functions
         ├── pareto_test.py                     <- Unitary tests for pareto functions
         ├── simulated_annealing_test.py        <- Unitary tests for simulated annealing
         ├── simulated_annealing_II_test.py     <- Unitary tests for simulated annealing II
         │
         ├── crossover_tests                    <- Inputs and outputs for crossover tests
         ├── mating_tests                       <- Inputs and outputs for mating tests
         ├── mutation_tests                     <- Inputs and outputs for mutation tests
         ├── survivor_tests                     <- Inputs and outputs for survivor tests
         ├── nsga_II_tests                      <- Inputs and outputs for nsga_II tests
         ├── pareto_tests                       <- Inputs and outputs for pareto tests
         ├── simulated_annealing_tests          <- Inputs and outputs for simulated annealing tests
         └── simulated_annealing_II_tests       <- Inputs and outputs for simulated annealing II tests
 

    

```

General-purpose toolbox for implementing a vectorized genetic algorithm (GAs). Binary and permutation representations are available to the maximization of a fitness function, i.e. a function provided by users. Several genetic operators are available and can be combined to explore the best settings for the current task. Furthermore, users can define new genetic operators and easily evaluate their performances. Local search using simulated annealing algorithm can be applied to exploit interesting regions. GAs can be run sequentially or in parallel.

## Usage

```
ga(problem_type = "binary" or "perm", 
   fitness_class,
   pop_size, num_variables,
   max_iteration = 10,
   suggestion_solutions = None,
   crossover_operator = "obx" or "single_point"
   mutation_operator =  "displacement" or  "bit_inversion"
   mating_operator = "roulette_wheel"
   survivor_operator = "fitness_based"
   prob_crossover = 0.8, 
   prob_mutation = 0.1, 
   keep_best = False,
   ls_call = False,
   parallel_call = False)
```

## Settings

### Required arguments:

- problem_type : type of genetic algorithm to be run depending on the nature of decision variables. Possible values are:
"binary" for binary representations of decision variables.
"perm" for problems that involves reordering of a list of objects.

- fitness_class : object from "Objective Function" class. This function considers as input, a vector with numerical values that represents a potential solution. It returns a numerical value called  “fitness”.

- pop_size : population size.

- num_variables : number of decision variables.

### Optional arguments:

- max_iteration: maximum number of iterations to run before the GA search is halted, default value is set to 10.

- suggestion_solutions: a matrix of user provided solutions and included in the initial population.

- crossover_operator = an Python function performing crossover, i.e. a function which forms offsprings by combining part of the genetic information from their parents. See Genetic Operators for available functions.

- mutation_operator = an Python function performing mutation, i.e. a function which randomly alters the values of some genes in a parent chromosome. See Genetic Operators for available functions.

- mating_operator = an Python function performing mating selection, i.e. process of selecting parents which mate and recombine to create off-springs for the next generation. See Genetic Operators for available functions.

- survivor_operator = an Python function performing selection, i.e. a function which determines which individuals are to be kicked out and which are to be kept in the next generation. See Genetic Operators for available functions.

- prob_crossover = probability of crossover between pairs of chromosomes. Typically this is a large value and by default is set to 0.8.

- prob_mutation = probability of mutation in a parent chromosome. Usually mutation occurs with a small probability, and by default is set to 0.1.

- keep_best = logical argument specifying if best solutions at each iteration should be saved in a slot called best_solutions.

- ls_call = logical specifying whether or not a local search using Simulated Annealing Algorithm should be used.

- parallel_call = optional argument which allows to specify if the Genetic Algorithm should be run sequentially or in parallel.

## Genetic Operators  

### Survivor:
- age_based
- fitness_based
- nsgaII: Multiobjective survivor based on pareto fronts and crowding distance for selecting tied solutions within the same front. As our standard for problems via genetic algorithm is to maximize, the nsgaII criterion is also maximization as a default. If NSGA II is chosen as the survivor operator, fitness class' attribute "type" should be "multi".

### Mating:
- roulette_wheel
- ranking
- tournament
- truncation
- sus

### Crossover:
Permutation problems:
- pmx
- pmx_2
- ox
- ox_2
- obx
- cycle

Binary problems:
- single_point
- uniform

### Mutation:
Permutation problems:
- swap
- insert
- scramble
- inversion
- displacemen
- reverse

Binary problems:
- bit_inversion
