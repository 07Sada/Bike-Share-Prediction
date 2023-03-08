import os, sys 
from bike.logger import logging
from bike.exception import BikeException
from bike.entity import config_entity, artifact_entity
from bike.components.data_ingestion import DataIngestion

print(__name__)
if __name__=="__main__":
     try:
          training_pipeline_config = config_entity.TrainingPipelineConfig()

          # data ingestion 
          data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
          data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
          data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

     except Exception as e:
          raise BikeException(e, sys)