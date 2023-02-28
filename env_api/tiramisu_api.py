from env_api.core.services.converting_service import ConvertService
from env_api.data.data_service import DataSetService
from env_api.core.services.tiramisu_service import *
from env_api.scheduler.models.action import *
from env_api.scheduler.models.schedule import Schedule
from env_api.scheduler.services.scheduler_service import SchedulerService
import os


class TiramisuEnvAPIv1:
    def __init__(self):
        # The services of the environment
        self.dataset_service: DataSetService = None
        self.scheduler_service: SchedulerService = SchedulerService()
        self.tiramisu_service: TiramisuService = TiramisuService()
        # init database
        self.init_dataset_service(
            dataset_path="env_api/data/dataset/", copy_path="env_api/data/copy/"
        )
        # a list of programs of the dataset
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
        # Get the file path for the program with the given name
        file_path = self.dataset_service.get_file_path(name)
        # Load the Tiramisu model from the file
        tiramisu_prog = self.tiramisu_service.get_tiramisu_model(path=file_path)
        # Create a Schedule object for the Tiramisu model
        schedule = Schedule(tiramisu_prog)
        # Use the Scheduler service to set the schedule for the Tiramisu model
        comps_tensor, loops_tensor = self.scheduler_service.set_schedule(
            schedule_object=schedule
        )
        # Convert the schedule to a tree representation using the Convert service
        return ConvertService.get_encoded_rl_representation(
            comps_tensor, loops_tensor, schedule
        )

    def parallelize(self, loop_level: int):
        # Create a Parallelization action with the given loop level
        parallelization = Parallelization(params=[loop_level], name="Parallelization")
        # Use the Scheduler service to apply the Parallelization action to the schedule
        return self.scheduler_service.apply_action(parallelization)
