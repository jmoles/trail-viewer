from deap import algorithms, base, creator, tools
import random
from scoop import futures
import timeit

from AgentNetwork import AgentNetwork
from AgentTrail import AgentTrail

NUM_MOVES = 250
POP_SIZE  = 300
NGEN      = 20

# Configure DEAP
creator.create("FitnessMulti", base.Fitness, weights=(1,-1))
creator.create("Individual", list, fitness=creator.FitnessMulti)

def runMaze(individual):
    an = AgentNetwork()
    at = AgentTrail()
    at.readTrail("trails/john_muir_32.yaml")

    num_moves = 0

    an.network._setParameters(individual)

    for _ in xrange(NUM_MOVES):
        if at.getFoodStats()[1] == 0:
            break

        currMove = an.determineMove(at.isFoodAhead())

        if(currMove == 1):
            at.turnLeft()
        elif(currMove == 2):
            at.turnRight()
        elif(currMove == 3):
            at.moveForward()

        num_moves = num_moves + 1

    return (at.getFoodConsumed(), num_moves)

if __name__ == '__main__':
    start = timeit.default_timer()

    an = AgentNetwork()

    toolbox = base.Toolbox()
    toolbox.register("map", futures.map)

    toolbox.register("attr_float", random.uniform, a=-5, b=5)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
        toolbox.attr_float, n=len(an.network.params))
    toolbox.register("population", tools.initRepeat, list,
        toolbox.individual)

    toolbox.register("evaluate", runMaze)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population(n=POP_SIZE)
    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=NGEN)
    print(tools.selBest(pop, k=1)[0])

    # Print the best network
    an = AgentNetwork()
    at = AgentTrail()
    at.readTrail("trails/john_muir_32.yaml")

    an.network._setParameters(tools.selBest(pop, k=1)[0])

    for _ in xrange(NUM_MOVES):
        currMove = an.determineMove(at.isFoodAhead())

        if(currMove == 1):
            at.turnLeft()
        elif(currMove == 2):
            at.turnRight()
        elif(currMove == 3):
            at.moveForward()

    print at.getFoodConsumed()
    at.printDataMatrix()

    stop = timeit.default_timer()

    print "Runtime: " + str(stop - start)
