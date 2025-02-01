import sys
import os
from dataclasses import dataclass

import pandas as pd 
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
 
from src.logger import logging
from src.exception import CustomException

from src.utils import save_object



@dataclass
class DataTranformationConfig:
    preprocessor_obj_path=os.path.join('artifacts',"preprocessor.pkl")
    
class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTranformationConfig()
    
    def get_data_transformation_object(self):
        try:
            numerical_colms=["writing_score","reading_score"]
            categorical_colms=[
                "gender",
                'lunch',
                'race_ethnicity',
                'parental_level_of_education',
                'test_preparation_course',
            ]
            
            num_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy='median')),
                    ("scaler", StandardScaler())
                ]
            )
            cat_pipeline=Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('encoding',OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )
            logging.info(f"Categorical Features : {categorical_colms}")
            logging.info(f"Numerical features: {numerical_colms}")
            preprocessor=ColumnTransformer(
                [
                    ("numerical",num_pipeline,numerical_colms),
                    ("categorical",cat_pipeline,categorical_colms)
                ]
            )
            
            return preprocessor
            
        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            
            logging.info("Successfully read training and test data")
            
            logging.info("Obtaining preprocessing object")
            
            preprocessing_obj=self.get_data_transformation_object()
            
            target_feature="math_score"
            input_train_feature = train_df.drop(columns=[target_feature],axis=1)
            target_train_feature=train_df[target_feature]
            
            input_test_feature = test_df.drop(columns=[target_feature],axis=1)
            target_test_feature=test_df[target_feature]
            
            logging.info("Applying preprocessor on the training and testing dataframe")
            
            input_train_arr=preprocessing_obj.fit_transform(input_train_feature)
            input_test_arr=preprocessing_obj.transform(input_test_feature)
            
            train_arr=np.c_[ 
                            input_train_arr,np.array(target_train_feature)
                            ]
            test_arr=np.c_[ 
                            input_test_arr,np.array(target_test_feature)
                            ]
            logging.info("Saved preprocessing objext.")
            
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_path,
                obj=preprocessing_obj
            )
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_path,
            )
            
        except Exception as e:
            raise CustomException(e,sys)