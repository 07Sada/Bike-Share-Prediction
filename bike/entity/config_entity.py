import os, sys 
from bike.logger import logging 
from bike.exception import BikeException
from datetime import datetime

FILE_NAME = "bike.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = 'test.csv'

class TrainingPipelineConfig:
    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(), 'artifact', f"{datetime.now().strftime('%m_%d_%Y__%I_%M_%S')}")
        except Exception as e:
            raise BikeException(e, sys)

class DataIngestionConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
            try:
                self.database_name = "bike_demand_prediction"
                self.collection_name = 'bike'

                # creating data_ingestion directory
                self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir, 'data_ingestion')

                # creating feature store file path 
                self.feature_store_file_path = os.path.join(self.data_ingestion_dir,'feature_store',FILE_NAME)

                # creating train_file_path 
                self.train_file_path = os.path.join(self.data_ingestion_dir,'dataset',TRAIN_FILE_NAME)

                # creating test_file_path 
                self.test_file_path = os.path.join(self.data_ingestion_dir,'dataset',TEST_FILE_NAME)

                # test_size while splitting the dataset
                self.test_size = 0.2
            except Exception as e:
                    raise BikeException(e, sys)
    
    def to_dict(self)->dict:
        try:
            return self.__dict__
        except Exception as e:
            raise BikeException(e, sys)