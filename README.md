# simulation-manager
An abstract class for simulations that keeps basic housekeeping, including logging and configuration management.

## Usage Instructions

The `SimulationManager` class is designed to serve as a base class for managing simulations. It provides essential housekeeping functionalities such as initialization, running, cleanup, logging, and configuration management. To use the `SimulationManager` class, you need to inherit from it and implement the abstract methods specific to your simulation.

### Steps to Use
1. Create a new class that inherits from `SimulationManager`.
2. Implement the required abstract methods such as `initialize`, `run`, and `cleanup`.
3. Pass a configuration dictionary and optional logging information when instantiating your derived class.
4. Call the `run` method to execute the simulation.

### Logging Information (`log_info`)

The `log_info` parameter is an optional string input that provides additional context for logging during the simulation. It can be used to control the verbosity or type of logs generated.

- If `log_info` contains the substring `'test'`, the simulation will create a `test` directory for data.
- If `log_info` contains the substring `'debug'`, the simulation will enable debug-level logging, providing detailed information about the simulation's internal state and operations.

This parameter allows for flexible logging configurations, making it easier to debug or test simulations without modifying the core logic.

### Default Parameters (`default_params`)

Each simulation class that inherits from `SimulationManager` must define a `default_params` dictionary. This dictionary contains the default values for all parameters required by the simulation. It ensures that the simulation has a baseline configuration, which can be overridden by user-provided settings in the `config` dictionary.

The `default_params` dictionary is merged with the user-provided `config` during initialization, allowing for a flexible and consistent parameter management system.

For example:
```python
class MySimulation(SimulationManager):
    default_params = {
        "param_a": 10,
        "param_b": 20,
        "enable_feature_x": True
    }

    def __init__(self, config, seed=None, log_info=None):
        super().__init__(config, seed, log_info)
        # Access merged parameters
        print(f"Final Parameters: {self.params}")
```

By defining `default_params`, you ensure that your simulation has a complete set of parameters, even if some are not explicitly provided by the user.
### Attributes and Their Usage

The `SimulationManager` class provides several attributes to manage and organize simulation data effectively. Below is a description of these attributes and their functions:

- **`config` (dict)**:  
    This dictionary contains the configuration settings for the simulation. It is passed during initialization and can include parameters such as simulation name, maximum iterations, logging preferences, and other user-defined settings.

- **`params` (dict)** :  
    A dictionary that merges default simulation parameters with user-provided configurations. This ensures that the simulation has a complete set of parameters, with user inputs overriding defaults where applicable. Must be provided in the `config` dictionary.

- **`trial` (int)**:  
    Represents the current trial number for the simulation. A separate directory is created for each trial, and the trial number is also used as the seed for random number generation. This ensures reproducibility of results across different runs.

- **`data_loc` (str)**:  
    Specifies the base directory where all simulation data will be stored. This provides a centralized location for organizing simulation outputs. Must be provided in the `config` dictionary.

- **`sim_dir` (str)**:  
    The name of the directory specific to the simulation. This is used to differentiate between multiple simulations within the base directory. If it is not, provided, a default `sim_dir` is created using current timestamp.

- **`sim_path` (str)**:  
    The full path to the simulation directory for the current trial. It combines `data_loc` and `sim_dir` to create a unique path for storing trial-specific data.

- **`hdf5_path` (str)**:  
    The full path to the HDF5 file used for storing simulation data. This file format is efficient for managing large datasets and ensures that simulation results are stored in a structured and accessible manner.

These attributes collectively enable efficient management of simulation configurations, data storage, and reproducibility, making the `SimulationManager` class a robust framework for simulation development.

### Description in Configuration (`description`)

The `description` key in the `config` dictionary is used to provide a brief description of the simulation. If this key is included, its value will be written into the README file for the simulation. This allows users to document the purpose or details of the simulation directly within the configuration.

- If the `description` key is provided, its content will be added to the README file. Otherwise, a generic message, "No description provided," will be written into the README file.

This feature ensures that each simulation is well-documented and provides context for its purpose, even if no explicit description is given.

### Example

Below is an example of how to use the `SimulationManager` class:

```python
from manager import SimulationManager

class MySimulation(SimulationManager):
    default_params = {
        "a": 10,
        "b": 20,
        "enable_feature_x": True
    }

    def __init__(self, config, seed=None, log_info=None):
        super().__init__(config, seed, log_info)

        # Print all attributes provided by the SimulationManager class
        print(f"Config: {self.config}")
        print(f"Params: {self.params}")
        print(f"Trial: {self.trial}")
        print(f"Data Location: {self.data_loc}")
        print(f"Simulation Directory: {self.sim_dir}")
        print(f"Simulation Path: {self.sim_path}")
        print(f"HDF5 Path: {self.hdf5_path}")

        print("Initializing simulation...")
        self.data = [1, 2, 3, 4, 5]

    def run(self):
        print("Running simulation...")
        self.results = [x * 2 for x in self.data]
        print(f"Simulation results: {self.results}")

    def cleanup(self):
        print("Cleaning up simulation...")
        del self.data
        del self.results


# Instantiate and run the simulation
if __name__ == "__main__":
    # Example configuration dictionary
    config = {
        "description": "Testing MySimulation",
        "simulation_name": "ExampleSimulation",
        "max_iterations": 10,
        "enable_logging": True,
        "data_loc": 'data',
        "params": {
            "a": 1,
            "b": 2
        }
    }

    sim = MySimulation(config=config, seed=42, log_info="test_debug")
    print(f"Simulation Name: {sim.config['simulation_name']}")
    print(f"Max Iterations: {sim.config['max_iterations']}")
    print(f"Logging Enabled: {sim.config['enable_logging']}")
    sim.run()
```

### Output
When you run the above code, you will see the following output:
```
Initializing simulation...
Simulation Name: ExampleSimulation
Max Iterations: 10
Logging Enabled: True
Running simulation...
Simulation results: [2, 4, 6, 8, 10]
Cleaning up simulation...
```

This demonstrates the basic workflow of using the `SimulationManager` class. The example highlights how to utilize configuration and logging to enhance the simulation's utility. Customize the `initialize`, `run`, and `cleanup` methods to suit your specific simulation requirements.