import numpy as np

from libensemble import Ensemble
from libensemble.alloc_funcs.start_only_persistent import only_persistent_gens
from libensemble.specs import ExitCriteria, AllocSpecs, SimSpecs, GenSpecs
from simulator import mnist_training_sim
from generator import optimize_cnn

if __name__ == "__main__":

    # Create the ensemble
    ensemble = Ensemble(parse_args=True)

    ensemble.libE_specs.gen_on_manager = True
    
    user = {"num_networks": ensemble.nworkers}

    sim_specs = SimSpecs(sim_f=mnist_training_sim, user=user)
    gen_specs = GenSpecs(gen_f=optimize_cnn, user=user)
    alloc_specs = AllocSpecs(alloc_f=only_persistent_gens, user={"alt_type": True})

    ensemble.sim_specs = sim_specs
    ensemble.gen_specs = gen_specs
    ensemble.alloc_specs = alloc_specs
    ensemble.exit_criteria = ExitCriteria(sim_max=8)

    ensemble.run()
    ensemble.save_output(__file__)
