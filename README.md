## STGFA-SMOG Prototype
STGFA-SMOG: Search-based Test Generation Framework for Android Apps with Support for Multi-objective Generation
This is a prototype of search-based test generation framework for Android apps with support for multi-objective generation and addition of fitness functions over time. The prototype generates multi-objective test cases for Android GUI-based testing using search-based approach. The prototype uses a third party tool called [ ACVTool](https://github.com/pilgun/acvtool) to measure code coverage.
## Installation
### Environment Configration
* Python: 2.7
* Java version 1.8
* Android SDK: API 28
* Linux OS

Install Python dependencies:

    sudo pip install -r requirements.txt

Install ACVTool: To install ACVTool follow instructions given in the following link.
    [ ACVTool](https://github.com/pilgun/acvtool)

## Usage
### Settings
Before starting STGFA-SMOG the following parameters in settings.py should be set.
* FITNESS_FUNCS
* ACVTOOL\_WDIR 
* ACVTOOL\_CMDDIR

### Start STGFA-SMOG
    python main.py <apk_path>

### Limitations
This prototype performs best if:
* The Android app does not require the user to login.

## Output
Output content:

    /batt_usage - Battery usage logs of each test case.
    /cpu_usage_stats - CPU usage logs of each test case.
    /crash_logs - Crash logs and their corresponding test cases that lead to the crashes.
    /fitness_values - Fitness values of the fitness functions for each test case in each generation.
    /intermediate - Logbook of the genetic evolution.
    /mem_usage_stats - Memory usage logs of each test case.
    /net_usage - Network usage logs of each test case.
    /paretofront - Top 10 test cases of the whole generation or population.
    /population-scripts - Generated test cases for each generation.

## Notes
* FITNESS_FUNCS - This is the parameter where the combination of fitness functions to be used are configured, i.e. [crash, length, cpu|memory|network|battery|line|method|class]
* ACVTOOL\_WDIR - Set the directory where the instrumented APK will be saved when any of the code coverage fitness functions are selected.
* ACVTOOL\_CMDDIR - Specify the directory where the instrumented APK is found. This parameter is used in the ACVTool commands.
