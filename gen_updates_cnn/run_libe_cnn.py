import numpy as np

from libensemble import Ensemble
from libensemble.alloc_funcs.give_pregenerated_work import give_pregenerated_sim_work
from libensemble.specs import ExitCriteria, AllocSpecs, SimSpecs, GenSpecs
from simulator import mnist_training_sim

if __name__ == "__main__":

    n_samples = 4
    init_history = np.zeros(
        n_samples, dtype=[("weights", object), ("grad", object, (10, 128)), ("loss", float), ("sim_id", int)]
    )
    init_history["loss"] = [0.0] * n_samples
    init_history["sim_id"] = range(n_samples)

    # Create the ensemble
    ensemble = Ensemble(parse_args=True, H0=init_history)

    # Create the sim_specs
    sim_specs = SimSpecs()
    sim_specs.sim_f = mnist_training_sim
    sim_specs.inputs = ["weights"]

    # gen_specs = GenSpecs()
    # gen_specs.gen_f = "eval_cnn"
    # gen_specs.inputs = ["acc"]
    # gen_specs.outputs = [("weights", object)]

    alloc_specs = AllocSpecs()
    alloc_specs.alloc_f = give_pregenerated_sim_work

    ensemble.sim_specs = sim_specs
    # ensemble.gen_specs = gen_specs
    ensemble.alloc_specs = alloc_specs
    ensemble.exit_criteria = ExitCriteria(sim_max=4)

    ensemble.run()
    ensemble.save_output(__file__)
