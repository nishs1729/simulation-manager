import sys
from manager import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

class FHN(SimulationManager):
    ## Default simulation parameters
    default_params = {
        "a": 0.7,
        "b": 0.8,
        "tau": 12.5,
        "I": 0.5,
        "dt": 0.01,
        'y0': [0.1, 0.0],
        "tend": 100,
    }

    def __init__(self, config, seed=None, log_info=None):
        super().__init__(config, seed, log_info)

        self.method = self.config.get('method', False) or 'RK45'
        
        self.t = np.arange(0, self.tend+self.dt, self.dt)
        self.v = None
        self.w = None

    def fhn_system(self, t, y):
        v, w = y
        dv = v - (v ** 3) / 3 - w + self.I
        dw = (v + self.a - self.b * w) / self.tau
        return [dv, dw]

    def run(self):
        sol = solve_ivp(self.fhn_system, [0, self.tend], self.y0, 
                        t_eval=self.t, method=self.method)
        self.v, self.w = sol.y

    def save_data(self):
        # Save data to HDF5 file
        with h5py.File(self.hdf5_path, "w") as h5file:
            h5file.create_dataset("time", data=self.t)
            h5file.create_dataset("v", data=self.v)
            h5file.create_dataset("w", data=self.w)

        logging.info(f'saved simulation data to {self.hdf5_path}')

    def plot_results(self):
        fig, axs = plt.subplots(2,1, figsize=(6, 8))

        # Plot time series
        axs[0].plot(self.t, self.v, label="v (membrane potential)")
        axs[0].plot(self.t, self.w, label="w (recovery variable)")
        axs[0].set_xlabel("Time")
        axs[0].set_ylabel("Variables")
        axs[0].legend(frameon=False)

        # Plot phase portrait
        axs[1].plot(self.v, self.w, label="Trajectory")

        # Plot nullclines
        v_nullcline = np.linspace(-2, 2, 500)

        # Nullcline for dv/dt = 0
        w_v_nullcline = v_nullcline - (v_nullcline ** 3) / 3 + self.I
        axs[1].plot(v_nullcline, w_v_nullcline, 'r--', label="dv/dt = 0")

        # Nullcline for dw/dt = 0
        w_w_nullcline = (v_nullcline + self.a) / self.b
        axs[1].plot(v_nullcline, w_w_nullcline, 'b--', label="dw/dt = 0")

        axs[1].set_xlabel("v (membrane potential)")
        axs[1].set_ylabel("w (recovery variable)")
        axs[1].legend(frameon=False)

        for ax in axs:
            ax.spines[['top', 'right']].set_visible(False)

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    config = {
        'description': 'Testing',
        'sim_dir': 'dfgdfg',
        "data_loc": "data/",
        'params': {
            'tend': 200,
            'b': 1.0,
            'y0': [0.1, 0.5,]
        }
    }

    try:
        seed = int(sys.argv[1])
    except IndexError:
        seed = 42  # Default seed value
    except ValueError:
        print(f"Invalid seed (must be integer). Setting, seed = 42")
        seed = 42

    model = FHN(config, seed=seed, log_info='')
    model.run()
    # model.plot_results()
    model.save_data()