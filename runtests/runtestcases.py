import sys, os, glob

from runtests.adbcommands import adb_shell_input_cmd
from fitness_functions.fitnessfactory import FitnessFunctionFactory
from fitness_functions.cpu_usage_fitness import CpuUsage
from fitness_functions.memory_usage_fitness import MemoryUsage
from fitness_functions.crash_fitness import Crashes
from fitness_functions.testcase_length_fitness import TestcaseLength
from fitness_functions.network_usage_fitness import NetworkUsage
from fitness_functions.battery_usage_fitness import BatteryUsage
from fitness_functions.line_coverage_fitness import LineCoverage
from fitness_functions.method_coverage_fitness import MethodCoverage
from fitness_functions.class_coverage_fitness import ClassCoverage
from acvtool.acvtool_commands import acvtool
from app_info.check_app_running import app_crashed
import settings

def run_test_case(individual, package_name, index_indv, gen, app_name):
    fitfactory = FitnessFunctionFactory(individual, package_name, index_indv, gen)
    fitnessess = fitfactory.get_fintess_functions(settings.FITNESS_FUNCS)

    # Check if valid number of fitness functions are returned
    if len(fitnessess) < 1:
        print("No appropraite fitness functions are chosen")
        sys.exit()
    
    # Variable for fitness valuses
    fitness_values = []

    # Count the number of times CPU and Memory inf is queried
    cpu_info_counter = 0
    mem_info_counter = 0
    net_info_counter = 0
    batt_info_counter = 0

    # Store the total CPU and Memory usage
    total_cpu_used = 0
    total_memory_used = 0
    total_network_used = 0.0
    total_battery_used = 0.0

    print("Running test cases...")
    
    # Send the sequence of atomic event to the AUT
    for index, line in enumerate(individual):
        app_crashed(package_name)
        adb_shell_input_cmd(line)
        if ((index+1) % settings.CPU_INTERVAL == 0) and "cpu" in settings.FITNESS_FUNCS:
            for fit in fitnessess:
                if(isinstance(fit, CpuUsage)):
                    total_cpu_used = total_cpu_used + fit.getFitness_value()
                    cpu_info_counter = cpu_info_counter + 1
        
        if ((index+1) % settings.MEM_INTERVAL == 0) and "memory" in settings.FITNESS_FUNCS:
            for fit in fitnessess:
                if(isinstance(fit, MemoryUsage)):
                    total_memory_used = total_memory_used + fit.getFitness_value()
                    mem_info_counter = mem_info_counter + 1
        
        if ((index+1) % settings.NET_INTERVAL == 0) and "network" in settings.FITNESS_FUNCS:
            for fit in fitnessess:
                if(isinstance(fit, NetworkUsage)):
                    total_network_used = total_network_used + fit.getFitness_value()
                    net_info_counter = net_info_counter + 1
        
        if ((index+1) % settings.BATT_INTERVAL == 0) and "battery" in settings.FITNESS_FUNCS:
            for fit in fitnessess:
                if(isinstance(fit, BatteryUsage)):
                    total_battery_used = total_battery_used + fit.getFitness_value()
                    batt_info_counter = batt_info_counter + 1
    
    for fit in fitnessess:
        if isinstance(fit, CpuUsage):
            if cpu_info_counter != 0:
                total_cpu_used = total_cpu_used / cpu_info_counter
            fitness_values.append(total_cpu_used)
            # Check if a file exists
            if len(os.listdir('cpu_usage_stats/') ) != 0:
                files = glob.glob('cpu_usage_stats/*')
                for f in files:
                    os.remove(f)

        elif isinstance(fit, MemoryUsage):
            if mem_info_counter != 0:
                total_memory_used = total_memory_used / mem_info_counter
            fitness_values.append(total_memory_used)
    
        elif isinstance(fit, Crashes):
            fitness_values.append(fit.getFitness_value())

        elif isinstance(fit, TestcaseLength):
            fitness_values.append(fit.getFitness_value())
        
        elif isinstance(fit, NetworkUsage):
            if net_info_counter != 0:
                total_network_used = total_network_used / net_info_counter
            fitness_values.append(total_network_used)
            # Check if a file exists
            if len(os.listdir('net_usage/') ) != 0:
                files = glob.glob('net_usage/*')
                for f in files:
                    os.remove(f)
        
        elif isinstance(fit, BatteryUsage):
            if batt_info_counter != 0:
                total_battery_used = total_battery_used / batt_info_counter
            fitness_values.append(total_battery_used)
            # Check if a file exists
            if len(os.listdir('batt_usage/') ) != 0:
                files = glob.glob('batt_usage/*')
                for f in files:
                    os.remove(f)
        
        elif isinstance(fit, LineCoverage):
            acvtool(app_name, package_name, individual)
            fitness_values.append(fit.getFitness_value())
        
        elif isinstance(fit, MethodCoverage):
            acvtool(app_name, package_name, individual)
            fitness_values.append(fit.getFitness_value())
        
        elif isinstance(fit, ClassCoverage):
            acvtool(app_name, package_name, individual)
            fitness_values.append(fit.getFitness_value())

    return tuple(fitness_values)

