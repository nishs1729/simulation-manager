import os, h5py, logging, json
from abc import ABC, abstractmethod
from datetime import datetime
import numpy as np

class SimulationManager(ABC):
    """
    SimulationManager is an abstract base class designed to manage simulation configurations, 
    data paths, and inputs. It provides a structured framework for setting up simulations, 
    handling configurations, creating necessary directories, and logging simulation details.

    Attributes:
        config (dict): The configuration dictionary for the simulation.
        params (dict): A dictionary containing simulation parameters, merged from default 
            parameters and user-provided configurations.
        trial (int): A separate directory is created based on trial. It is also used as the
            seed for random number generation, used to ensure reproducibility.
        data_loc (str): The base directory where simulation data will be stored.
        sim_dir (str): The name of the simulation directory.
        sim_path (str): The full path to the simulation directory for the current trial.
        hdf5_path (str): The full path to the HDF5 file used for storing simulation data.

    Methods:
        __init__(config, seed, log_info):
            Initializes the SimulationManager instance, sets up configurations, directories, 
            and logging, and saves the configuration.
        _set_config(config):
            Sets the configuration and parameters for the simulation. Accepts either a 
            dictionary or a path to a JSON file.
        _setup_directories(log_info):
            Creates necessary directories for the simulation, sets up logging, and initializes 
            files like Readme.md and an HDF5 file for storing data.
        _setup_logging(log_info):
            Configures logging for the simulation, with options for different logging levels 
            based on the provided log_info.
        _save_config():
            Saves the merged configuration and parameters to a JSON file in the simulation 
            directory.
        run():
            Abstract method that must be implemented by subclasses to execute the simulation.
    """

    def __init__(self, config, seed, log_info):
        """
        Initialize the SimulationManager instance.

        Args:
            config (dict or str): Configuration dictionary or path to a JSON file.
            seed (int): Seed for random number generation to ensure reproducibility.
            log_info (str): Logging configuration information.
        """
        ## Set up the configuration and parameters
        self._set_config(config)

        ## Set the random seed for reproducibility
        self.trial = seed if seed else 1
        np.random.seed(self.trial)

        ## Set attributes from the merged parameter dictionary
        for key, value in self.params.items():
            setattr(self, key, value)

        ## Set up directories and logging
        self._setup_directories(log_info)

        ## Save the configuration to a file
        self._save_config()

    def _set_config(self, config):
        """
        Set the configuration and parameters for the simulation.

        Args:
            config (dict or str): Configuration dictionary or path to a JSON file.

        Raises:
            ValueError: If the provided config is neither a dictionary nor a valid file path.
        """
        ## Load the configuration from a dictionary or JSON file
        if isinstance(config, dict):
            self.config = config
        elif isinstance(config, str) and os.path.isfile(config):
            with open(config, 'r') as f:
                self.config = json.load(f)
        else:
            raise ValueError("Config must be a dictionary or a valid path to a JSON file.")
        
        ## Ensure the subclass has a 'default_params' attribute and merge it with the provided params
        assert hasattr(self, 'default_params') and isinstance(getattr(self, 'default_params'), dict), \
            f"{self.__class__} must have a dictionary 'default_params'!"
        self.params = self.default_params.copy()
        self.params.update(self.config['params'])

    def _setup_directories(self, log_info):
        """
        Set up the data directory for the simulation.

        Args:
            log_info (str): Logging configuration information.
        """
        ## Determine the base data location
        self.data_loc = self.config['data_loc']

        ## Determine the simulation directory name
        if 'test' in log_info:
            self.sim_dir = 'test'
        elif 'sim_dir' in self.config and self.config['sim_dir']:
            self.sim_dir = self.config['sim_dir']
        else:
            ## Default simulation directory name based on timestamp
            self.sim_dir = f"sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        ## Create the full simulation path for the current trial
        self.sim_path = os.path.join(self.data_loc, self.sim_dir, f"trial_{self.trial}")
        os.makedirs(self.sim_path, exist_ok=True)

        ## Set up logging for the simulation
        self._setup_logging(log_info)

        ## Create a 'Readme.md' file and write the simulation description
        readme_path = os.path.join(os.path.dirname(self.sim_path), "Readme.md")
        with open(readme_path, "w") as readme_file:
            print(self.config['description'])
            if 'description' in self.config and bool(self.config['description']):
                desc = self.config['description']
                print("dlfghsdkljfghsldkfg")
            else:
                desc = "No description provided."
            readme_file.write(desc)

        ## Create an HDF5 file for storing simulation data
        self.hdf5_path = os.path.join(self.sim_path, f"data_{self.trial}.hdf5")
        with h5py.File(self.hdf5_path, "w") as h5file:
            pass  ## Create an empty HDF5 file

        ## Log the setup details
        logging.info(f"Simulation directory: '{self.sim_path}'.")

    def _setup_logging(self, log_info):
        """
        Configure logging for the simulation.

        Args:
            log_info (str): Logging configuration information.
        """
        ## Set the default logging level and log file path
        level = logging.INFO
        filename = os.path.join(self.sim_path, 'sim.log')

        ## Adjust logging level if 'debug' is specified
        if 'debug' in log_info:
            level = logging.DEBUG

        ## Configure the logging settings
        logging.basicConfig(level=level, filename=filename, filemode="w",
                            format="%(asctime)s.%(msecs)03d [%(funcName)s] %(levelname)s: %(message)s",
                            datefmt='%H:%M:%S')

    def _save_config(self):
        """
        Save the merged configuration and parameters to a JSON file.
        """
        ## Update the configuration with the merged parameters
        self.config['params'] = self.params

        ## Save the configuration to a JSON file
        config_path = os.path.join(os.path.dirname(self.sim_path), "config.json")
        with open(config_path, "w") as config_file:
            json.dump(self.config, config_file, indent=4)

        ## Log the configuration save operation
        logging.info(f"Saved config to '{config_path}'.")

    @abstractmethod
    def run(self):
        """
        Execute the simulation. This method must be implemented by subclasses.
        """
        pass