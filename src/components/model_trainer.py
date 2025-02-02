import sys
import os
from src.exception import CustomException
from src.logger import logging

from sklearn.linear_model import LinearRegression,Ridge,Lasso
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor,GradientBoostingRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor

from sklearn.metrics import r2_score
from src.utils import save_object,evaluate_model
from dataclasses import dataclass

#from src.components.data_tranformation import DataTransformation
#from src.components.data_tranformation import DataTranformationConfig

@dataclass
class ModelTrainerConfig:
    model_train_path=os.path.join("artifacts",'model.pkl')
    
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()
    try:    
        def initiate_model_trainer(self,train_arr,test_arr):
            logging.info("Spliting training and test data")
            X_train,y_train,X_test,y_test=(
            train_arr[:,:-1],
            train_arr[:,-1],
            test_arr[:,:-1],
            test_arr[:,-1],
            )        

            models={
                "Linear Regreesion": LinearRegression(),
                "Lasso": Lasso(),
                "Ridge": Ridge(),
                "SVM": SVR(),
                "KNN" : KNeighborsRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Random Forest": RandomForestRegressor(),
                "Gradient Boost": GradientBoostingRegressor(),
                "Ada boost": AdaBoostRegressor(),
                "XGboost": XGBRegressor(),
                "Catboost": CatBoostRegressor(),
            }
            model_report:dict=evaluate_model(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models)
    
            best_score = max(sorted(model_report.values()))
            best_model_name= list(model_report.keys())[list(model_report.values()).index(best_score)]
            best_model= models[best_model_name]
        
            if best_score<0.60:
                raise CustomException("No best model found")
            logging.info(f"Best model found on training and testing datasets")
        
            save_object(
                file_path=self.model_trainer_config.model_train_path,
                obj=best_model
            )
            predicted=best_model.predict(X_test)
            r2_sqaure= r2_score(y_test,predicted)
        
            return r2_sqaure
    
    
    
    except Exception as e:
        raise CustomException(e,sys)