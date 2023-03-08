import pymongo 
import pandas as pd 
import json 
from bike.config import mongo_client

DATA_FILE_PATH = "/config/workspace/Bike Share Prediction.csv"
DATABASE_NAME = 'bike_demand_prediction'
COLLECTION_NAME ='bike'

if __name__ == '__main__':
    df = pd.read_csv(DATA_FILE_PATH)
    print(f"Data Loaded successfully")
    print(f"Shape of the dataset: {df.Shape}")

    # converting dataframe to json format so that we can dump the record in mongo db
    df.reset_index(drop=True, inplace=True)

    json_record = list(json.loads(df.T.to_json()).values())
    #df.T.json() transposing the dataframe and converting to json format
    #json.loads() function converts the json string to python dictonary
    #values method of dictonary is called which return a list of all the values in the dictonary
    #list function is used to convert the returned values to list

    mongo_client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)
    print("Data Dumped Successfully")
