import os, sys 
from bike.logger import logging
from bike.exception import BikeException
import pandas as pd 
import numpy as np 
from bike.config import mongo_client
from typing import Optional,List
import yaml
import dill 

def get_collection_as_dataframe(database_name:str, collection_name:str)->pd.DataFrame:
    """ 
    Description: This function return collection as dataframe
    =========================================================
    database_name : database name 
    collection_name : collection name
    ========================================================
    return Pandas dataframe of a collection
    """

    try:
        logging.info(f"Reading data from database :[{database_name}] and collection : [{collection_name}]")

        # creating dataframe from mongodb data
        df:pd.DataFrame = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Data Loaded Successfully to pandas dataframe, size of the data: [{df.shape}]")

        # dropping "_id" columns from dataframe 
        if "_id" in df.columns:
            logging.info(f"Removing the '_id' column from database")
            df.drop("_id", axis=1, inplace=True)
        
        return df 

    except Exception as e: 
        raise BikeException(e, sys)

def write_yaml_file(file_path,data:dict):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)
        with open(file_path,"w") as file_writer:
            yaml.dump(data,file_writer)
    except Exception as e: 
        raise BikeException(e, sys)

def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise BikeException(e, sys)from e

def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of utils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Exited the save_object method of utils")
    except Exception as e:
        raise BikeException(e, sys)from e

def remove_outlier_IQR(df):
    try:
        # Calculate the first quartile of the data
        Q1 = df.quantile(0.25)
        # Calculate the third quartile of the data
        Q3 = df.quantile(0.75)
        # Calculate the interquartile range
        IQR = Q3 - Q1
        # Create a new DataFrame that contains only rows where the values are not outliers
        df1 = df[~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR)))]
        # Return the new DataFrame
        return df1
    except Exception as e:
        raise BikeException(e, sys)from e

def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise BikeException(e, sys)

def load_object(file_path: str, ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise BikeException(e, sys) from e
