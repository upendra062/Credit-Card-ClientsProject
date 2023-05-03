import sys
import os
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from src.utils import load_object

class PredictPipeline:
    def __init__(self):
        pass
    def predict(self, features):
        try:
            preprocessor_path = os.path.join('artifacts', 'preprocessor.pkl')
            model_path = os.path.join('artifacts','model.pkl')
            
            preprocessor = load_object(preprocessor_path)
            model=load_object(model_path)

            data_scaled = preprocessor.transform(features)

            pred = model.predict(data_scaled)
            return int(pred)
        except Exception as e:
            logging.info("Exception occured in prediction")
            raise CustomException(e,sys)
        
class CustomData:
    def __init__(self,
                 X1:float,
                 X2:float,
                 X3:float,
                 X4:float,
                 X5:float,
                 X6:float,
                 X7:float,
                 X8:float,
                 X9:float,
                 X10:float,
                 X11:float,
                 X12:float,
                 X13:float,
                 X14:float,
                 X15:float,
                 X16:float,
                 X17:float,
                 X18:float,
                 X19:float,
                 X20:float,
                 X21:float,
                 X22:float,
                 X23:float,
                 ):
        self.X1 = X1  
        self.X2 = X2 
        self.X3 = X3
        self.X4 = X4
        self.X5 = X5 
        self.X6 = X6 
        self.X7 = X7 
        self.X8 = X8 
        self.X9 = X9
        self.X10 = X10
        self.X11 = X11 
        self.X12 = X12 
        self.X13 = X13
        self.X14 = X14  
        self.X15 = X15
        self.X16 = X16  
        self.X17 = X17  
        self.X18 = X18  
        self.X19 = X19  
        self.X20 = X20  
        self.X21 = X21  
        self.X22 = X22  
        self.X23 = X23

    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                'X1':[self.X1],
                'X2':[self.X2], 
                'X3' :[self.X3],
                'X4':[self.X4],
                'X5':[self.X5],
                'X6':[self.X6],
                'X7':[self.X7],
                'X8':[self.X8],
                'X9':[self.X9],
                'X10':[self.X10],
                'X11':[self.X11],
                'X12':[self.X12],
                'X13':[self.X13],
                'X14':[self.X14],
                'X15':[self.X15],
                'X16':[self.X16],
                'X17':[self.X17],
                'X18':[self.X18],
                'X19':[self.X19],
                'X20':[self.X20],
                'X21':[self.X21],
                'X22':[self.X22],
                'X23':[self.X23],
            }
            df = pd.DataFrame(custom_data_input_dict)
            logging.info('DataFrame Gathered')
            return df

        except Exception as e:
            logging.info("Exception Occured in prediction pipeline")
            raise CustomException(e, sys)