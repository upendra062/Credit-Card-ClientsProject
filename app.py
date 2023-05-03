from flask import Flask , request, render_template 
from src.pipeline.prediction_pipeline import CustomData, PredictPipeline
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.logger import logging
import pandas as pd
from urllib.request import urlopen as uReq
from flask_cors import cross_origin
from bs4 import BeautifulSoup as bs
import requests

application = Flask(__name__)
app = application

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/result')
def resultPage():
    if request.method=='GET':
        show = 'You have not run the prediction'
        return render_template('result.html', show=show)
    
@app.route('/data')
def csv_to_html():
    data = pd.read_csv("data/newcreditclient.csv")
    data = data[:100]
    return render_template('data.html',result=[data.to_html(index=False)])

@app.route('/train')
def train_data():
    try:
        obj = DataIngestion()   
        train_data_path, test_data_path = obj.initiate_data_ingestion()
        data_transformation = DataTransformation()
        train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data_path, test_data_path)
        model_trainer=ModelTrainer()
        model_trainer.initate_model_training(train_arr, test_arr)
        context = "Your Model is trained Successful"
        return render_template('index.html',context=context) 
    except:
        logging.info('Error In Training Model')
        

@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method=='GET':
        return render_template('form.html')
    else:
        data = CustomData(   
                 X1=float(request.form.get('X1')),
                 X2=float(request.form.get('X2')),
                 X3=float(request.form.get('X3')),
                 X4=float(request.form.get('X4')),
                 X5=float(request.form.get('X5')),
                 X6=float(request.form.get('X6')),
                 X7=float(request.form.get('X7')),
                 X8=float(request.form.get('X8')),
                 X9=float(request.form.get('X9')),
                 X10=float(request.form.get('X10')),
                 X11=float(request.form.get('X11')),
                 X12=float(request.form.get('X12')),
                 X13=float(request.form.get('X13')),
                 X14=float(request.form.get('X14')),
                 X15=float(request.form.get('X15')),
                 X16=float(request.form.get('X16')),
                 X17=float(request.form.get('X17')),
                 X18=float(request.form.get('X18')),
                 X19=float(request.form.get('X19')),
                 X20=float(request.form.get('X20')),
                 X21=float(request.form.get('X21')),
                 X22=float(request.form.get('X22')),
                 X23=float(request.form.get('X23'))
        )
        final_new_data = data.get_data_as_dataframe()
        predict_pipeline = PredictPipeline()
        pred = predict_pipeline.predict(final_new_data)
        # if pred==0:
        #     pred = 'YES'
        # elif pred==1:
        #     pred = 'NO'
        # else:
        #     print('no result found')
        results = pred

        Congratulations = 'Congratulations'
        return render_template('result.html', final_result = results, Congratulations=Congratulations)


@app.route('/reviewhome',methods=['GET'])  
@cross_origin()
def homePage():
    return render_template("review_index.html")

@app.route('/review',methods=['POST','GET']) 
@cross_origin()
def reviews():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()
            flipkart_html = bs(flipkartPage, "html.parser")
            bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
            del bigboxes[0:3]
            box = bigboxes[0]
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
            prodRes = requests.get(productLink)
            prodRes.encoding='utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            commentboxes = prod_html.find_all('div', {'class': "_16PBlm"})
            filename = 'review_data/' + searchString + ".csv"
            fw = open(filename, "w")
            headers = "Product, Customer Name, Rating, Heading, Comment \n"
            fw.write(headers)
            reviews = []
            for commentbox in commentboxes:
                try:
                    name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
                except:
                    name = 'No Name'
                try:
                    rating = commentbox.div.div.div.div.text
                except:
                    rating = 'No Rating'
                try:
                    commentHead = commentbox.div.div.div.p.text

                except:
                    commentHead = 'No Comment Heading'
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': ''})
                    custComment = comtag[0].div.text
                except Exception as e:
                    print("Exception while creating dictionary: ",e)

                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}
                reviews.append(mydict)

            return render_template('review_result.html', reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    else:
        return render_template('review_result.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=5000, 
            debug=True)