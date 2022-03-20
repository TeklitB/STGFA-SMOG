# use headless evaluator
HEADLESS = False

# === Emulator ===
DEVICE_NUM = 1
AVD_BOOT_DELAY = 60
AVD_SERIES = "api28_"
EVAL_TIMEOUT = 120

# GA parameters
SEQUENCE_LENGTH_MIN = 20
SEQUENCE_LENGTH_MAX = 50
POPULATION_SIZE = 20
OFFSPRING_SIZE = 20
NGENERATION = 30
# Crossover probability
CXPB = 0.3
# Mutation probability
MUTPB = 0.3
# Reproduction probability
REPROPB = 0.15
# Diversification probability
# Covers the remaining percent

# Query CPU  and memory usage at a specified interval
CPU_INTERVAL = 3
MEM_INTERVAL = 3
NET_INTERVAL = 3
BATT_INTERVAL = 3

# Fitness Function Constants
CRASH = "crash"
LENGTH = "length"
CPU = "cpu"
MEMORY = "memory"
NETWORK = "network"
BATTERY = "battery"
LINECOVERAGE = "line"
METHODCOVERAGE = "method"
CLASSCOVERAGE = "class"

# Configure combination of fitness function to use e.g ["length", "crash", "cpu"|"memory"]
FITNESS_FUNCS = ["crash", "length", "battery"]

# Configure fitness weights
# crash, testcase_length, cpu|memory (order does matter) 1.0, -1.0, 1.0
FITNESS_WEIGHTS = (1.0, -1.0, 1.0,)

# Top best individuals to return
BEST_INDIV = 10

# ACVTool working directory
ACVTOOL_WDIR = "/home/tbg/acvtool/acvtool_working_dir/"
ACVTOOL_CMDDIR = "~/acvtool/acvtool_working_dir/"