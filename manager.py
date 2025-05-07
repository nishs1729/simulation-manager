import os, h5py, logging, json
from abc import ABC, abstractmethod
from datetime import datetime
import numpy as np

class SimulationManager(ABC):
    """
    Abstract base class for managing simulation configurations, data paths, and inputs.
    """

    def __init__(self, config, seed, log_info):
        self._set_config(config)

        ## Set seed for random numbers
        self.trial = seed if seed else 1
        np.random.seed(self.trial)

        ## Set attributes from the merged parameter dictionary
        for key, value in self.params.items():
            setattr(self, key, value)

        self._setup_directories(log_info)
        self._save_config()

    def _set_config(self, config):
        """
        Set the configuration and params for the simulation.

        Args:
            config (dict or str): Configuration dictionary or path to a JSON file.

        Raises:
            ValueError: If the provided config is neither a dictionary nor a valid file path.
        """
        ## Set self.config
        if isinstance(config, dict):
            self.config = config
        elif isinstance(config, str) and os.path.isfile(config):
            with open(config, 'r') as f:
                self.config = json.load(f)
        else:
            raise ValueError("Config must be a dictionary or a valid path to a JSON file.")
        
        ## Create new dict with default params and update with provided params
        assert hasattr(self, 'default_params') and isinstance(getattr(self, 'default_params'), dict), \
            f"{self.__class__} must have a dictionary 'default_params'!"
        self.params = self.default_params.copy()
        self.params.update(self.config['params'])

    def _setup_directories(self, log_info):
        """
        Set up the data directory for the simulation.
        """
        ## Create the new data directory
        self.data_loc = self.config['data_loc']
        if 'test' in log_info:
            self.sim_dir = 'test'
        elif 'sim_dir' in self.config and self.config['sim_dir']:
            self.sim_dir = self.config['sim_dir']
        else:
            self.sim_dir = f"sim_{datetime.now().strftime("%Y%m%d_%H%M%S")}"

        self.sim_path = os.path.join(self.data_loc, self.sim_dir)
        os.makedirs(self.sim_path, exist_ok=True)

        ## Setup logging
        self._setup_logging(log_info)

        ## Create a 'Readme.md' file and write the description
        readme_path = os.path.join(self.sim_path, "Readme.md")
        with open(readme_path, "w") as readme_file:
            readme_file.write(self.config['description'])

        ## Create hdf5 file for storing simulation data
        self.hdf5_path = os.path.join(self.sim_path, f"data_{self.trial}.hdf5")
        with h5py.File(self.hdf5_path, "w") as h5file: pass
        
        ## Log the setup
        logging.info(f"Simulation directory: '{self.sim_path}'.")

    def _setup_logging(self, log_info):
        level = logging.INFO
        filename = os.path.join(self.sim_path, 'sim.log')
        if 'debug' in log_info:
            level = logging.DEBUG

        logging.basicConfig(level=level, filename=filename, filemode="w",
                            format="%(asctime)s.%(msecs)03d [%(funcName)s] %(levelname)s: %(message)s",
                            datefmt='%H:%M:%S')

    def _save_config(self):
        ## Update config with params and save in json file
        self.config['params'] = self.params
        config_path = os.path.join(self.sim_path, "config.json")
        with open(config_path, "w") as config_file:
            json.dump(self.config, config_file, indent=4)

        logging.info(f"Saved config to '{config_path}'.")

    @abstractmethod
    def initialize_simulation(self):
        """
        Initialize simulation-specific parameters and state.
        """
        pass

    @abstractmethod
    def run(self):
        """
        Execute the simulation.
        """
        pass