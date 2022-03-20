import numpy, time, shutil
import os, sys, subprocess
from datetime import datetime

from deap import base
from deap import creator
from deap import tools

from app_info import retrieve_package_name
from devices import emulator
from input_events import get_events
from input_events import test_seq_generator
from algorithm import eaMuPlusLambdaAlgo
from runtests import adbcommands
from resetAUT import reset_app_state
import settings

        
# Fitness evaluation function
def evaluate_test_case(individual, package_name, index_indv, gen, app_name):
    # rund suite on device
    fitness_values = reset_app_state.setup_aut(individual, package_name, index_indv, gen, app_name)

    return fitness_values

def mutate_test_case(individual, indpb):
    #shuffle sequence of test cases
    individual, = tools.mutShuffleIndexes(individual, indpb)
    
    # Mutate events by changing their parameters
    for i in range(len(individual)):
        atomic_event = individual[i]
        action = atomic_event.split()[0]
        new_atomic_event = get_events.get_events_by_actiontype(action)
        individual[i] = new_atomic_event
    
    return individual,

def return_as_is(a):
	return a

if not isinstance(settings.FITNESS_FUNCS, list):
    print("Invalid Fitness functions configuration.\n"+
    "Fitness functions chosen must be provided as a list e.g. ['crash', 'length', 'cpu']\n"+
    "Provided Fitness Functions are type of {}: {}".format(type(settings.FITNESS_FUNCS), settings.FITNESS_FUNCS))
    sys.exit()

if not isinstance(settings.FITNESS_WEIGHTS, tuple):
    print("Invalid Fitness functions configuration.\n"+
    "Fitness weights must be provided as a tuple e.g. (1.0, -1.0, 1.0)\n"+
    "Provided Fitness Weights are type of {}: {}".format(type(settings.FITNESS_WEIGHTS), settings.FITNESS_WEIGHTS))
    sys.exit()

if len(settings.FITNESS_FUNCS) != len(settings.FITNESS_WEIGHTS):
    print("Invalid Fitness functions configuration.\n"+
    "Number of fitness functions chosen and fitness weights given does not match\n"+
    "Fitness Functions: {} Fitness Weights: {}".format(settings.FITNESS_FUNCS, settings.FITNESS_WEIGHTS))
    sys.exit()

if len(settings.FITNESS_FUNCS) < 1 or len(settings.FITNESS_WEIGHTS) < 1:
    print("Invalid Fitness functions configuration.\n"+
    "Number of fitness functions to choose or fitness weights to give is one at minimum and three at maximum\n"+
    "Fitness Functions: {0}, Fitness Weights: {1}".format(settings.FITNESS_FUNCS, settings.FITNESS_WEIGHTS))
    sys.exit()

if len(settings.FITNESS_FUNCS) > 3 or len(settings.FITNESS_WEIGHTS) > 3:
    print("Invalid Fitness functions configuration.\n"+
    "Number of fitness functions to choose or fitness weights to give is one at minimum and three at maximum\n"+
    "Fitness Functions: {0} Fitness Weights: {1}".format(settings.FITNESS_FUNCS, settings.FITNESS_WEIGHTS))
    sys.exit()

creator.create("FitnessMax", base.Fitness, weights=settings.FITNESS_WEIGHTS)
#Create Individual class that encapsulate our individuals
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("individual", test_seq_generator.gen_test_seq)
toolbox.register("population", tools.initRepeat, list, toolbox.individual) 

toolbox.register("evaluate", evaluate_test_case)
toolbox.register("mate", tools.cxUniform, indpb=0.5)
toolbox.register("mutate", mutate_test_case, indpb=0.5)
toolbox.register("select", tools.selNSGA2)

# Log the history
history = tools.History()
# Decorate the variation operators
toolbox.decorate("mate", history.decorator)
toolbox.decorate("mutate", history.decorator)

def main(app_path):

    startTime = datetime.now()
    current_time = startTime.strftime("%H:%M:%S")
    print("Start time: {0}".format(current_time))

    if not os.path.exists(app_path):
        print("The app does not exist!\n")
        sys.exit()

    # Extract app file name
    app_name = app_path.split("/")[-1].split(".")[0]

    # Get package name of the app app-debug.apk Amazon_App.apk
    byte_package_name, app_dir = retrieve_package_name.get_package_name(app_path)
    package_name = byte_package_name.decode('utf-8')
    print("Package name: ", package_name)

    # Boot the emulator first
    emulator.boot_devices()

    print("Emulator booting completed.")

    # Uninstall the AUT if it already exists
    adbcommands.uninstall_app(package_name)

    # If code coverage measure is needed, Instrument the app with ACVTool
    if "line" in settings.FITNESS_FUNCS or "method" in settings.FITNESS_FUNCS or "class" in settings.FITNESS_FUNCS:
        # Delete acvtool working directory if it exists
        if os.path.exists(settings.ACVTOOL_WDIR):
            shutil.rmtree(settings.ACVTOOL_WDIR, ignore_errors=False, onerror=None)
        
        # Instrument the app
        print("Instrumenting ...")
        inst_proc = subprocess.Popen("acv instrument {0}".format(app_path), 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        inst_apk_output, inst_apk_err = inst_proc.communicate()

        # Install the instrumented apk
        instal_proc = subprocess.Popen("acv install {0}".format(settings.ACVTOOL_CMDDIR+"instr_"+app_name+".apk"), 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        instal_apk_output, instal_apk_err = instal_proc.communicate()
        #print("Installation Error =>", instal_apk_err)   

    # Otherwise, simply install the original app
    else:
        # Install the app
        adbcommands.install_app(app_path)
        time.sleep(1)

    population = toolbox.population(n=settings.POPULATION_SIZE)
    
    history.update(population)

    #hall_of = tools.ParetoFront()
    hall_of = tools.HallOfFame(maxsize=settings.BEST_INDIV)
    
    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    # axis = 0, the numpy.mean will return an array of results
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)
    stats.register("pop_fitness", return_as_is)

    #evolve the population
    population, logbook = eaMuPlusLambdaAlgo.evolve_pop(population, toolbox, settings.POPULATION_SIZE, settings.OFFSPRING_SIZE,
                                                cxpb=settings.CXPB, mutpb=settings.MUTPB, repropb=settings.REPROPB, ngen=settings.NGENERATION,
                                                package_name=package_name, app_name=app_name, stats=stats, halloffame=hall_of, verbose=True)

    pareto_front = "paretofront/nondominated_testcases.txt"
    check_path = os.path.exists(pareto_front)
    open_paretofront = open(pareto_front, "a" if check_path else "w+")
    for ind in hall_of:
        open_paretofront.write(str(ind)+" "+str(ind.fitness.values)+"\n")
    
    endTime = datetime.now()
    current_end_time = endTime.strftime("%H:%M:%S")
    print("End time: {0}".format(current_end_time))

if __name__=="__main__":
    if len(sys.argv) <= 1:
        print("APK path missed.\nPlease provide the required commandline arguments.")
        sys.exit()
    apk_path = sys.argv[1]
    main(apk_path)

