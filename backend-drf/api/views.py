from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import StockPredictionSerializer
from rest_framework import status
from rest_framework.response import Response 
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
from django.conf import settings
from .utils import save_plot
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model

# Create your views here.

class StockPredictionAPIView(APIView):
    def post(self,request):
        serializer = StockPredictionSerializer(data=request.data)
        if serializer.is_valid():
            ticker=serializer.validated_data['ticker']

            # Fetch the data from yfinance
            now=datetime.now()
            start=datetime(now.year-10,now.month,now.day)
            end=now
            df=yf.download(ticker,start,end)
            print(df)
            if df.empty:
                return Response({'error':'No data found for the given ticker','status':status.HTTP_404_NOT_FOUND})
            
            # Flatten the MultiIndex and remove the ticker (second level)
            df.columns = df.columns.get_level_values(0)  # Get only the first level (Price type)
            # Remove the column name (Price)
            df.columns.name = None
            df=df.reset_index()

            # Generate basic plot
            plt.switch_backend('AGG')
            plt.figure(figsize=(12,5))
            plt.plot(df.Date,df.Close, label='Closing Price')
            plt.title(f"Closing price of {ticker}")
            plt.xlabel('Date')
            plt.ylabel('Close price')
            plt.legend()
            # Save the plot to a file
            plot_img_path = f'{ticker}_plot.png'
            image_path=os.path.join(settings.MEDIA_ROOT,plot_img_path)
            plt.savefig(image_path)
            plt.close()
            plot_img=settings.MEDIA_URL + plot_img_path
            # print(plot_img)

            # 100 Days moving average
            ma100=df['MA_100']=df.Close.rolling(100).mean()
            plt.switch_backend('AGG')
            plt.figure(figsize=(12,5))
            plt.plot(df.Close, label='Price')
            plt.plot(ma100,'r',label='100 DMA')
            plt.title(f"100 Days Moving Average of {ticker}")
            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.legend()

            plot_img_path=f'{ticker}_100_dma.png'
            plot_100_dma=save_plot(plot_img_path)

            # 200 Days moving average
            ma200=df['MA_200']=df.Close.rolling(200).mean()
            plt.switch_backend('AGG')
            plt.figure(figsize=(12,5))
            plt.plot(df.Close, label='Closing Price')
            plt.plot(ma100,'r',label='100 DMA')
            plt.plot(ma200,'g',label='200 DMA')
            plt.title(f"200 Days Moving Average of {ticker}")
            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.legend()

            plot_img_path=f'{ticker}_200_dma.png'
            plot_200_dma=save_plot(plot_img_path)

            # Splitting data into Training & Testing datasets
            data_training = pd.DataFrame(df.Close[0:int(len(df)*0.7)])
            data_testing = pd.DataFrame(df.Close[int(len(df)*0.7): int(len(df))])

            # Scalling down the data between 0 and 1
            scaler = MinMaxScaler(feature_range=(0,1))

            # Load ML Model
            model=load_model('stock_prediction_model.keras')
            
            # Preparing Test Data
            past_100_days=data_training.tail(100)
            final_df=pd.concat([past_100_days,data_testing],ignore_index=True)
            input_data=scaler.fit_transform(final_df)

            x_test=[]
            y_test=[]

            for i in range(100,input_data.shape[0]):
                x_test.append(input_data[i-100:i])
                y_test.append(input_data[i,0])

            x_test,y_test = np.array(x_test),np.array(y_test)

            # Making Predictions
            y_predicted=model.predict(x_test)

            # Revert the scaled prices to original price
            y_predicted=scaler.inverse_transform(y_predicted.reshape(-1,1)).flatten()
            y_test=scaler.inverse_transform(y_test.reshape(-1,1)).flatten()

            # print('y_predicted==>',y_predicted)
            # print('y_test==>',y_test)

            # Plot the final prediction

            return Response({'status':'success', 'plot_img':plot_img,'plot_100_dma':plot_100_dma,'plot_200_dma':plot_200_dma})
