# Advanced-Programming-Project-HSG
For our project we have decided to code a prototype of a WebApplication which allows Swiss homeowners to get a quick prediction of the price of their property based on its characteristics (e.g. square-meters, location, etc.) as well as a comparison to the market. The predictive model is a Random Forest, which we have trained with data that we scraped (April 2024) from [Immoscout24.ch](https://www.immoscout24.ch/en), the leading Swiss real estate market place.

Authors of this project are: 
- Yves Grädel (yves.graedel@student.unisg.ch)
- Jonas Lehmann (jonas.lehmann@student.unisg.ch)
- Marc Berger (marc.berger@student.unisg.ch)

This file provides a description of the project and is structured as follows: 
- Demonstration of the Front End of the Web Application 
- How to run the code
- Descriprion of the different files

## Disclaimer
This project has been realized with the help of online sources such as https://stackoverflow.com/ and with the help of OpenAIs' LLM ChatGPT 4 (https://chatgpt.com/). 

## 1) Demonstration of the Front End of the Web App
Click on the image below to see the demo. Please do not share the video or the link to it.

[![Watch the video](http://img.youtube.com/vi/k0ZD0h8pN6M/0.jpg)](https://youtu.be/k0ZD0h8pN6M)

## 2) How to run the code

The code used to scrape the data (NAME), clean the data (NAME) and fit the predictive model (NAME) can be run independently from the code used to create the WebApp.

### 2.1) WebApp
In order to run the WebApp, it is important to keep the project files in the correct structure: 
![image](https://github.com/graeyv/Advanced-Programming-Project-HSG/assets/161760200/48aaf3a7-c5ed-4e14-a34b-1790df104efe)

The Repository is currently organized in this way. However, due to a restriction of the file sizes two placeholders (adr_data_clean_EXAMPLE.csv & best_random_forest_model_PLACEHOLDER.pkl.txt) have been added to the Repo instead of the correct files. These should be replaced and renamed accordingly (adr_data_clean_EXAMPLE.csv & best_random_forest_model_PLACEHOLDER.pkl):
- The correct .csv file of the Swiss addresses register can be downladed from https://www.swisstopo.admin.ch/de/amtliches-verzeichnis-der-gebaeudeadressen
- The correct .pkl file can directly be generated directly using the (NAME) script.

Moreover, it is important to download all the necessary packages which are imported at the top of the respective scripts. Once this is all done, the WebAPP can be started by running the app.py script. Clicking on the link appearing in the console output will open the App in the default browser of your machine: 

![image](https://github.com/graeyv/Advanced-Programming-Project-HSG/assets/161760200/62a31850-8933-4c95-8cc1-b7985e011839)

### 2.2) WebScrapper
TO BE COMPLETED

### 2.3) ETC...

## 3) Description of all files
### 3.1) data
#### 3.1.1) 
#### 3.1.2) 
### 3.2) model
#### 3.2.1) best_random_forest_model.pkl
#### 3.2.2) feature_columns.pkl 
### 3.3) static
### 3.4) templates
#### 3.4.1) about.html
#### 3.4.2) analytics.html
#### 3.4.3) base.html
#### 3.4.4) contact.html
#### 3.4.5) property.html



