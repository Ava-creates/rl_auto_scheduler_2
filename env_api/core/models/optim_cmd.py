from env_api.scheduler.models.action import *


class OptimizationCommand:
    def __init__(self, action: Action, comps):
        self.params_list = action.params
        self.action = action
        self.comps = comps
        self.tiramisu_optim_str = self.get_tiramisu_optim_str()

    def get_tiramisu_optim_str(self):
        """Convert the optimization command into Tiramisu code.
        Returns:
            str: The tiramisu snippet that represents the optimization command.
        """
        if isinstance(self.action, Interchange):
            interchange_str = (
                ".interchange(" + ",".join([str(p) for p in self.params_list]) + ");"
            )
            optim_str = ""
            for comp in self.comps:
                optim_str += "\n\t {}".format(comp) + interchange_str
            return optim_str
        elif isinstance(self.action, Skewing):
            assert len(self.params_list) == 4
            skewing_str = ".skew(" + ",".join([str(p) for p in self.params_list]) + ");"
            optim_str = ""
            for comp in self.comps:
                optim_str += "\n\t {}".format(comp) + skewing_str
            return optim_str

        elif isinstance(self.action, Parallelization):
            assert len(self.params_list) == 1
            return (
                "\t"
                + self.comps[0]
                + ".tag_parallel_level("
                + str(self.params_list[0])
                + ");"
            )

        elif isinstance(self.action, Tiling):
            assert len(self.params_list) == 4 or len(self.params_list) == 6
            tiling_str = ".tile(" + ",".join([str(p) for p in self.params_list]) + ");"
            optim_str = ""
            for comp in self.comps:
                optim_str += "\n\t {}".format(comp) + tiling_str
            return optim_str
        elif isinstance(self.action, Unrolling):
            optim_str = ""
            for comp in self.comps:
                unrolling_str = (
                    ".unroll("
                    + ",".join([str(p) for p in self.params_list[comp]])
                    + ");"
                )
                optim_str += "\n\t {}".format(comp) + unrolling_str
            return optim_str
        elif isinstance(self.action, Reversal):
            reversal_str = ".loop_reversal(" + str(self.params_list[0]) + ");"
            optim_str = ""
            for comp in self.comps:
                optim_str += "\n\t {}".format(comp) + reversal_str
            return optim_str
        elif isinstance(self.action, Fusion):
            optim_str = ""
            prev_comp = self.comps[0]
            for comp in self.comps[1:]:
                optim_str += (
                    "\n\t {}".format(prev_comp)
                    + ".then("
                    + str(comp)
                    + ","
                    + str(self.params_list[0])
                    + ");"
                )
                prev_comp = comp
            return optim_str
