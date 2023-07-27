
## 1. Problem Statement

Predict the sales of bakery for N days in future

## 2. Soultion 

To create an ML model for prediction of sales for N days in the future.

## 3. Dataset

Dataset contains two columns
    - Column1 has the dates 
    - Column 2 has the number of sales a bakery does on a given day.

Sales data ranges from date `2018-10` to `2019-04`

## 4. Models

I have used `Linear regression` and `ARIMA` for model building.
AIRMA models are subset of Linear regression models. To go with base model I have seleted Linear regression
As our dataset contain time as feature, so to forecast it I have used ARIMA model.

## 5. Benchmark

|       Model       |   RMSE    |   MAE   |
| ----------------- | --------- | ------- |
|Linear Regression	| 18.016592 |12.823726|
|ARIMA	            | 18.026205 |13.966885|

## 6. Validation

`RMSE` and `MAE` value for Linear Regression model is less as compare to ARIMA. 
Also from graph of True prediction vs Actual data, we can see that for ARIMA model prediction values are constant and for Linear regresion we can see better prediction.

For final model selection I have selected Linear regression

## 7. Prediction

To make prediction run following command. It take number of days as argument

```
  python predict.py <num_of_day>
```

It will print dataframe with date and sales

|date          |    sales  |
| ------------ | --------- |
|0 2019-03-26  | 15.293161 |
|1 2019-03-27  | 13.462099 |
|2 2019-03-28  | 11.631037 |
|3 2019-03-29  |  9.799976 |
|4 2019-03-30  |  7.968914 |
