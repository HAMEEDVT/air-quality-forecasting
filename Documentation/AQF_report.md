# Air Quality Forecasting for Indian Cities Using Machine Learning

## 1. Introduction

Air pollution has become one of the most serious environmental issues affecting urban areas across the world, especially in rapidly developing countries such as India. Major cities like Delhi, Mumbai, Chennai, and Bangalore frequently experience high levels of particulate matter, particularly PM2.5, which poses severe risks to public health. Predicting air quality levels in advance can help governments, organizations, and individuals take preventive measures.

This project focuses on forecasting the Air Quality Index (AQI) for selected Indian cities using machine learning techniques. The system collects PM2.5 air pollution data from an external API and uses the Prophet forecasting model to predict future air quality trends. The final output is presented through an interactive web application built using Streamlit.

## 2. Problem Statement

Urban populations are increasingly exposed to hazardous air pollution levels. However, most people only receive real-time air quality information rather than future predictions. Without predictive insights, it becomes difficult for citizens and authorities to plan actions such as limiting outdoor exposure, issuing public warnings, or implementing pollution control measures.

The problem addressed in this project is the lack of accessible tools that can forecast future AQI levels based on historical air pollution data. This system aims to build a forecasting platform that predicts AQI trends for major Indian cities using machine learning and displays the results through an easy-to-use dashboard.

## 3. Objectives

The primary objectives of this project include:

* To collect air quality data for selected Indian cities.
* To preprocess and transform PM2.5 data into AQI values.
* To apply a machine learning forecasting model for predicting future pollution levels.
* To develop an interactive web application for visualizing historical and predicted AQI values.

## 4. System Architecture

The system consists of several key components that work together to perform data collection, forecasting, and visualization.

### 4.1 Data Source

The project uses the Open-Meteo Air Quality API to retrieve hourly PM2.5 concentration data. The API provides air quality estimates without requiring an API key, making it convenient for academic and research projects.

### 4.2 Data Processing

The retrieved hourly PM2.5 data is processed using the Pandas library. The system converts hourly data into daily averages to improve forecasting stability. After preprocessing, the PM2.5 values are converted into AQI values based on Indian National Air Quality Standards.

### 4.3 Forecasting Model

The forecasting model used in this project is Prophet, a time series forecasting library developed by Meta. Prophet is well suited for time series data that includes seasonal patterns and long-term trends. The model uses historical PM2.5 values to predict future pollution levels.

### 4.4 Visualization Layer

The final results are displayed using Streamlit and Plotly. Streamlit is used to create the web application interface, while Plotly generates interactive charts that show historical AQI values and predicted future trends.

## 5. Implementation Details

The project is implemented in Python using several libraries.

### 5.1 Streamlit

Streamlit is used to build the interactive web application. It provides the user interface components such as city selection, forecast duration sliders, charts, and tables.

### 5.2 Pandas

Pandas is used for handling and processing time series data. It is responsible for converting timestamps, resampling hourly data into daily averages, and preparing the dataset for model training.

### 5.3 Prophet Model

The Prophet model is trained on historical PM2.5 data. The dataset is formatted into two columns: "ds" representing the date and "y" representing the PM2.5 values. The model learns seasonal patterns such as yearly and weekly trends and generates predictions for future days.

### 5.4 Plotly Visualization

Plotly is used to generate an interactive visualization that displays:

* Historical AQI values
* Predicted AQI values
* Forecast uncertainty range

This helps users easily understand how air quality may change over time.

## 6. Working of the System

The working of the system can be summarized in the following steps:

1. The user selects a city from the Streamlit dashboard.
2. The system fetches PM2.5 air pollution data from the Open-Meteo API.
3. The retrieved hourly data is converted into daily averages.
4. PM2.5 values are transformed into AQI using Indian AQI conversion rules.
5. The Prophet model is trained using historical PM2.5 data.
6. The model generates predictions for the selected number of future days.
7. The results are displayed through interactive graphs and tables.

## 7. Results and Output

The system generates several outputs for the user:

* Current PM2.5 concentration level
* Current AQI value
* AQI category classification
* Historical AQI visualization
* Forecasted AQI values for future days
* A forecast table showing predicted PM2.5 and AQI levels

These outputs provide users with both current air quality conditions and future predictions.

## 8. Advantages of the System

The system offers several advantages:

* Provides future predictions instead of only real-time air quality data.
* Interactive visualization helps users easily understand pollution trends.
* Uses a reliable time series forecasting model.
* Can be extended to support additional cities.

## 9. Limitations

Despite its benefits, the system has certain limitations:

* The model relies on estimated data from the API rather than ground sensors.
* Forecast accuracy may vary depending on seasonal changes and sudden environmental factors.
* Only PM2.5 is considered when calculating AQI.

## 10. Future Enhancements

Several improvements can be implemented in the future:

* Incorporating additional pollutants such as PM10, NO2, and CO.
* Using deep learning models such as LSTM for improved prediction accuracy.
* Expanding the system to include more cities.
* Deploying the application on cloud platforms for public access.

## 11. Conclusion

Air quality forecasting is an important step toward improving public awareness and environmental monitoring. This project demonstrates how machine learning techniques can be used to analyze historical pollution data and generate future predictions. By combining data collection, forecasting, and visualization into a single application, the system provides a practical tool for understanding air pollution trends in major Indian cities.

The integration of Prophet forecasting with Streamlit visualization makes the system both powerful and easy to use. With further improvements and larger datasets, such systems can play a valuable role in environmental monitoring and decision making.
