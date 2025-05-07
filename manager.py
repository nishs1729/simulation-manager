import os
import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

class SimulationManager(ABC):
    """
    Abstract base class for managing simulation configurations, data paths, and inputs.
    """

    def __init__(self, config_path=None, data_dir="data", output_dir="output", sim_id=None):
        self.config_path = config_path
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.sim_id = sim_id or self._generate_sim_id()
        self.config = {}
        self.inputs = {}

        self._setup_directories()
        if self.config_path:
            self.load_config(self.config_path)

    def _generate_sim_id(self):
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def _setup_directories(self):
        """
        Create necessary directories for data and output.
        """
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_config(self, path):
        """
        Load configuration from a JSON file.
        """
        with open(path, 'r') as f:
            self.config = json.load(f)

    def save_config(self, path=None):
        """
        Save current configuration to a JSON file.
        """
        path = path or self.output_dir / f"{self.sim_id}_config.json"
        with open(path, 'w') as f:
            json.dump(self.config, f, indent=4)

    def load_inputs(self, input_file):
        """
        Load simulation inputs from a JSON file.
        """
        with open(input_file, 'r') as f:
            self.inputs = json.load(f)

    def save_inputs(self, path=None):
        """
        Save current inputs to a JSON file.
        """
        path = path or self.output_dir / f"{self.sim_id}_inputs.json"
        with open(path, 'w') as f:
            json.dump(self.inputs, f, indent=4)

    @abstractmethod
    def initialize_simulation(self):
        """
        Initialize simulation-specific parameters and state.
        """
        pass

    @abstractmethod
    def run_simulation(self):
        """
        Execute the simulation.
        """
        pass

    @abstractmethod
    def postprocess_results(self):
        """
        Post-process simulation results.
        """
        pass
