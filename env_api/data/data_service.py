from env_api.utils.config.config import Config
from .data_gen.tiramisu_maker import generate_programs
import pickle
from datetime import date


class DataSetService:
    def __init__(self,
                 dataset_path='env_api/data/dataset/',
                 offline_path=None):
        self.dataset_path = dataset_path
        self.offline_dataset = None
        self.offline_path = offline_path
        if (offline_path != None):
            with open(offline_path, "rb") as file:
                self.offline_dataset = pickle.load(file)

    def generate_dataset(self, size):
        generate_programs(output_path=self.dataset_path,
                          first_seed=10,
                          nb_programs=size)

    def get_file_path(self, func_name):
        file_name = func_name + "_generator.cpp"
        file_path = self.dataset_path + func_name + "/" + file_name
        exist_offline = False
        # Check if the file exists in the offline dataset
        if (self.offline_dataset):
            # Checking the function name
            exist_offline = func_name in self.offline_dataset
        return file_path, exist_offline

    def get_offline_prog_data(self, name: str):
        return self.offline_dataset[name]

    @classmethod
    def get_filepath(cls, func_name):
        '''
        This static class method is for the classes that need to get file path without the need to check in the offline dataset
        '''
        file_name = func_name + "_generator.cpp"
        file_path = Config.config.dataset.path + func_name + "/" + file_name
        return file_path

    def store_offline_dataset(self):
        if(self.offline_dataset):
            with open(self.offline_path[:-4] + date.today().__str__() +".pkl", "wb") as file:
                pickle.dump(self.offline_dataset,file)