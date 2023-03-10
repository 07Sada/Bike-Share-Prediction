from bike.entity import artifact_entity, config_entity
from bike import utils
from bike.exception import BikeException
from bike.logger import logging
from typing import Optional,List
import os, sys 
from sklearn.pipeline import Pipeline 
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pandas as pd 
import numpy as np 
from bike.config import TARGET_COLUMN, UNWANTED_COLUMNS, OUTLIER_COLUMNS, ONE_HOT_COLUMNS

class DataTransformation:
    def __init__(self, data_transformation_config:config_entity.DataTransformationConfig,
                        data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_transformation_config=data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact
        except Exception as e:
            raise BikeException(e, sys)
    
    
    def remove_outliers(self, df:pd.DataFrame, outlier_columns:List)->pd.DataFrame:
        # Use the previously defined remove_outlier_IQR function to remove outliers from the 'temp' column of the df DataFrame
        df_outlier_removed_TM = utils.remove_outlier_IQR(df[outlier_columns[0]])
        # Use the previously defined remove_outlier_IQR function to remove outliers from the 'hum' column of the df DataFrame
        df_outlier_removed_HM = utils.remove_outlier_IQR(df[outlier_columns[1]])

        # Convert the resulting Series to DataFrames
        df_outlier_removed_TM = pd.DataFrame(df_outlier_removed_TM)

        df_outlier_removed_HM = pd.DataFrame(df_outlier_removed_HM)
        
        # Find the indices of rows in df that are not in df_outlier_removed_TM
        ind_diff_SR = df.index.difference(df_outlier_removed_TM.index)
        # Find the indices of rows in df that are not in df_outlier_removed_HM
        ind_diff_WS = df.index.difference(df_outlier_removed_HM.index)

        # Convert the indices to sets
        in_first = set(ind_diff_SR)
        in_second = set(ind_diff_WS)
        # Find the union of the two sets of indices
        result = in_second.union(in_first)

        # Loop through the resulting set of indices
        if len(result)>0:
            for i in range(0, len(result), 1):
                # Drop the row at the current index from the df DataFrame
                df.drop(i, inplace=True)
            return df, result
        else:
            return df,result

    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        try:
            # Define the pipeline for one-hot encoding
            one_hot_pipeline = Pipeline([
                ('one_hot', OneHotEncoder(sparse=False, handle_unknown='ignore'))])

            # Define the pipeline for standard scaling
            standard_pipeline = Pipeline([
                                        ('standard', StandardScaler())])

            # Define the column transformer to apply the pipelines to the appropriate columns
            preprocessor = ColumnTransformer([
                ('one_hot_transformer', one_hot_pipeline, ONE_HOT_COLUMNS)
            ], remainder='passthrough')

            # Create the final pipeline
            pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('standard', standard_pipeline)])
            
            return pipeline
        except Exception as e:
            raise BikeException(e, sys)
                                                                                                                
    def initiate_data_transformation(self,) -> artifact_entity.DataTransformationArtifact:
        try:
            #reading training and testing file
            logging.info(f'Loading the train and test dataset from dataset')
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            logging.info(f"Train dataset size: {train_df.shape}")
            logging.info(f"test dataset size: {test_df.shape}")

            logging.info(f"Dropping target column, and creating input dataset")
            #selecting input feature for train and test dataframe
            input_feature_train_df=train_df.drop(TARGET_COLUMN,axis=1)
            input_feature_test_df=test_df.drop(TARGET_COLUMN,axis=1)

            logging.info(f"Dropping unwanted columns from the input dataset")
            # removing unwanted columns from the dataset
            input_feature_train_df = input_feature_train_df.drop(UNWANTED_COLUMNS, axis=1)
            input_feature_test_df = input_feature_test_df.drop(UNWANTED_COLUMNS, axis=1)

            # removing outliers from dataset 
            # remove_outliers = DataTransformation.remove_outliers()
            logging.info(f"removing outliers from the dataset")
            input_feature_train_df, train_df_outliers = self.remove_outliers(input_feature_train_df, OUTLIER_COLUMNS)
            logging.info(f"shape of input dataset after removing outlier train dataset: {input_feature_train_df.shape}")
            input_feature_test_df, test_df_outliers = self.remove_outliers(input_feature_test_df, OUTLIER_COLUMNS)
            logging.info(f"shape of input dataset after removing outlier test dataset: {input_feature_test_df.shape}")
            
            # selecting target feature for train and test dataframe
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]

            # removing outliers rows from target colum
            logging.info(f"Removing outlier rows from target column")
            target_feature_train_df = target_feature_train_df.drop(train_df_outliers)
            logging.info(f"Shape of the train target df after removing outliers: {target_feature_train_df.shape}")
            target_feature_test_df = target_feature_test_df.drop(test_df_outliers)
            logging.info(f"Shape of the test target df after removing outliers: {input_feature_test_df.shape}")

            transformation_pipleine = DataTransformation.get_data_transformer_object()
            transformation_pipleine.fit(input_feature_train_df)

            #transforming input features
            input_feature_train_arr = transformation_pipleine.transform(input_feature_train_df)
            input_feature_test_arr = transformation_pipleine.transform(input_feature_test_df)

            #target encoder
            train_arr = np.c_[input_feature_train_arr, target_feature_train_df.values ]
            test_arr = np.c_[input_feature_test_arr, target_feature_test_df.values]

            #save numpy array
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path,
                                        array=train_arr)

            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path,
                                        array=test_arr)

            utils.save_object(file_path=self.data_transformation_config.transform_object_path,
             obj=transformation_pipleine)

            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,
                transformed_train_path = self.data_transformation_config.transformed_train_path,
                transformed_test_path = self.data_transformation_config.transformed_test_path,
                )

            logging.info(f"Data transformation object generated")
            return data_transformation_artifact
        
        except Exception as e:
            raise BikeException(e, sys)