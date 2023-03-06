import traceback
from env_api.data.data_service import DataSetService
from env_api.core.services.tiramisu_service import *
from env_api.scheduler.models.action import *
from env_api.scheduler.models.schedule import Schedule
from env_api.scheduler.services.scheduler_service import SchedulerService
import os, torch

from env_api.utils.config.config import Config


class TiramisuEnvAPIv1:
    def __init__(self):
        # The services of the environment
        self.dataset_service: DataSetService = None
        self.scheduler_service: SchedulerService = SchedulerService()
        self.tiramisu_service: TiramisuService = TiramisuService()
        # Init database service with 2 paths :
        # - dataset_path : Contains the original program folder
        # - copy_path : Contains the path to store the chosen programs that are going to be optimized
        # This step of initializing the database service must be executed first in the init of tiramisu api
        self.init_dataset_service(
            dataset_path=Config.config.dataset.path,
            copy_path=Config.config.dataset.copy,
        )
        # The list of program names of the dataset
        self.programs = os.listdir(self.dataset_service.dataset_path)

    def init_dataset_service(self, dataset_path: str, copy_path: str):
        self.dataset_service = DataSetService(
            dataset_path=dataset_path, copy_path=copy_path
        )

    def get_programs(self):
        if self.programs == None:
            self.programs = os.listdir(self.dataset_service.dataset_path)
        return self.programs

    def set_program(self, name: str):
        # print("Choosing the function : ", name)
        # Get the file path for the program with the given name
        file_path = self.dataset_service.get_file_path(name)
        # Load the Tiramisu model from the file
        try:
            tiramisu_prog = self.tiramisu_service.get_tiramisu_model(path=file_path)
            # Create a Schedule object for the Tiramisu model
            schedule = Schedule(tiramisu_prog)
            # Use the Scheduler service to set the schedule for the Tiramisu model
            comps_tensor, loops_tensor = self.scheduler_service.set_schedule(
                schedule_object=schedule
            )
            # Using the model to embed the program in a 180 sized vector 
            with torch.no_grad():
                _, embedding_tensor = self.scheduler_service.prediction_service.get_speedup(
                    comps_tensor, loops_tensor, self.scheduler_service.schedule_object
                )
            return embedding_tensor
        except Exception as e:
            if isinstance(e, LoopsDepthException):
                print("Program has an unsupported loop level")
            elif isinstance(e, NbAccessException):
                print("Program has an unsupported number of access matrices")
            print("Traceback of the error : " + 60 * "-")
            print(traceback.print_exc())
            print(80 * "-")
            return None

    # TODO : for all these actions we need to generalize over computations and not over shared iterators

    def parallelize(self, loop_level: int):
        # print("Parallelization loop level : ",loop_level)
        # Create a Parallelization action with the given loop level
        parallelization = Parallelization(params=[loop_level])
        # Use the Scheduler service to apply the Parallelization action to the schedule
        return self.scheduler_service.apply_action(parallelization)

    def reverse(self, loop_level: int):
        # Create a Reversal action with given loop level
        reversal = Reversal(params=[loop_level])
        # Use the Scheduler service to apply the Reversal action to the schedule
        return self.scheduler_service.apply_action(reversal)
