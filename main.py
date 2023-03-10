import os, sys 
from bike.logger import logging
from bike.exception import BikeException
from bike.entity import config_entity, artifact_entity
from bike.components.data_ingestion import DataIngestion
from bike.components.data_validation import DataValidation
from bike.components.data_transformation import DataTransformation

print(__name__)
if __name__=="__main__":
     try:
          training_pipeline_config = config_entity.TrainingPipelineConfig()

          # data ingestion 
          data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
          data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
          data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

          # data Validation 
          data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
          data_validation = DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
          data_validation_artifact = data_validation.initiate_data_validation()

          #data transformation
          data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
          data_transformation = DataTransformation(data_transformation_config=data_transformation_config, 
          data_ingestion_artifact=data_ingestion_artifact)
          data_transformation_artifact = data_transformation.initiate_data_transformation()

     except Exception as e:
          raise BikeException(e, sys)