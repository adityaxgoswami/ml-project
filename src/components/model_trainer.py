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
                "Linear Regression": LinearRegression(),
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
            params={
                "Decision Tree": {
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    # 'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                 
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                
                "Linear Regression":{},
                
                "XGBRegressor":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "CatBoosting Regressor":{
                    'depth': [6,8,10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                "AdaBoost Regressor":{
                    'learning_rate':[.1,.01,0.5,.001],
                    # 'loss':['linear','square','exponential'],
                    'n_estimators': [8,16,32,64,128,256]
                }
                
            }
            model_report:dict=evaluate_model(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models,params=params)
    
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