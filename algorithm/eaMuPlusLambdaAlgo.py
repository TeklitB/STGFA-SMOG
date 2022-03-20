import random
import os
import pickle

from deap import tools

def log_selected_test_scripts(population, gen):
    for index_indv, indiv in enumerate(population):
        test_script_path = "population-scripts/atomicevent_script_"+str(gen)+str(index_indv)+".txt"
        check_path = os.path.exists(test_script_path)
        open_test_script_file = open(test_script_path, "a" if check_path else "w+")
        for atomic_event in indiv:
            open_test_script_file.write(atomic_event)
            open_test_script_file.write("\n")
        open_test_script_file.write(str(indiv.fitness.values))


def log_fitness_values(population, gen):
    fit_values_path = "fitness_values/fit_values_gen_"+str(gen)+".txt"
    check_path = os.path.exists(fit_values_path)
    open_fitvalues_file = open(fit_values_path, "a" if check_path else "w+")
    for indiv in population:
        for indx, val in enumerate(indiv.fitness.values):
            if indx == len(indiv.fitness.values)-1:
                open_fitvalues_file.write(str(val))
            else:
                open_fitvalues_file.write(str(val)+"\t")
        open_fitvalues_file.write("\n")

def evolve_pop(population, toolbox, mu, lambda_, cxpb, mutpb, repropb, 
                ngen, package_name, app_name, stats=None, halloffame=None, verbose=__debug__):
    
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    # Evaluate the individuals with invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = []
    for i in range(0, len(invalid_ind)):
        fitnesses.append(toolbox.evaluate(invalid_ind[i], package_name, i, 0, app_name))

    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit
    
    if halloffame is not None:
        halloffame.update(population)

    # ParetoFront
    #if halfm is not None:
        #halfm.update(population)
    
    record = stats.compile(population) if stats is not None else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print(logbook.stream)

    # Begin the generation process
    for gen in range(1, ngen + 1):
        # Vary the population
        offspring = varOr(population, toolbox, lambda_, cxpb, mutpb, repropb) 

        #Evaluate the individuals
        fitnesses = []
        for j in range(0, len(offspring)):
            fitnesses.append(toolbox.evaluate(offspring[j], package_name, j, gen, app_name))
        
        #fits = toolbox.map(toolbox.evaluate, offspring)
        for ind, fit in zip(offspring, fitnesses):
            ind.fitness.values = fit
        
        # Update the hall of fame with the newly generated individuals
        if halloffame is not None:
            halloffame.update(offspring)
        
        # ParetoFront
        #if halfm is not None:
            #halfm.update(offspring)

        # Assert all individuals have valid fitness
        invalid_ind_post = [ind for ind in population + offspring if not ind.fitness.valid]
        assert len(invalid_ind_post) == 0

        # Select the next generation population
        population = toolbox.select(population + offspring, mu)

        # log the test scripts
        log_selected_test_scripts(population, gen)

        # log the fitness values of the selected population
        log_fitness_values(population, gen)
        
        # Update the statistics with the new population
        record = stats.compile(population) if stats is not None else {}
        logbook.record(gen=gen, nevals=len(population), **record)
        if verbose:
            print(logbook.stream)
        
        # In case generation is interrupted
        logbook_path = "intermediate/logbook.pickle"
        if not os.path.exists(logbook_path):
            os.makedirs(logbook_path)

        #os.makedirs(os.path.dirname(logbook_path), exist_ok=True)
        logbook_file = open(logbook_path, "wb")
        pickle.dump(logbook, logbook_file)
        logbook_file.close()
    
    #print("ParetoFront :>")
    #print(halloffame)
    return population, logbook

def varOr(population, toolbox, lambda_, cxpb, mutpb, repropb):
    assert (cxpb + mutpb + repropb) < 1.0, ("The sum of the crossover, mutation and "+ 
    "reproduction probabilities must be smaller 1.0.")
    
    offspring = []
    for _ in range(lambda_):
        op_choice = random.random()
        # Apply crossover
        if op_choice < cxpb:
            ind1, ind2 = map(toolbox.clone, random.sample(population, 2))
            ind1, ind2 = toolbox.mate(ind1, ind2)
            del ind1.fitness.values
            offspring.append(ind1)
        # Apply mutation
        elif op_choice < cxpb + mutpb:
            ind = toolbox.clone(random.choice(population))
            ind, = toolbox.mutate(ind)
            del ind.fitness.values
            offspring.append(ind)
        # Apply reproduction
        elif op_choice < cxpb + mutpb + repropb:
            offspring.append(random.choice(population))
        # Introduce new individual to maintain diversity
        else:
            offspring.append(toolbox.individual())
    
    return offspring
