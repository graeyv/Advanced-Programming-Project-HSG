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
#### 3.1.1) adr_data_clean.csv
This is a .csv file containing the addresses of all buildings in Switzerland with the corresponding long/lat coordinates. As mentioned above the one in the repo is simply an example, the real .csv would need to run the app. 
#### 3.1.2) dat_clean.csv
This is the cleaned .csv file of the scraped data from immoscout24.ch. Each observation represents one property. (MAYBE SHORT DESCRIPTION OF VARS?)
### 3.2) model
#### 3.2.1) best_random_forest_model.pkl
This is a pickle file which contains the trained random forest model that is loaded into the app to make a prediction of the user's property price based on his/her input. The real file must be generated using the code (NAME) as the file in the repo is just a placeholder. 
#### 3.2.2) feature_columns.pkl 
This pickle file simply contains the variables which are actually used to train the model. For simplicity not all scraped data has been integrated into the WebApp and the predictive model. 
### 3.3) static
This folder contains all images (.png) which are used in the WebApp such as the avatars, the logo and name of the App, as well as the picture on the 'contact us' page.
### 3.4) templates
This folder contains the different HTML codes for the front end of the 4 pages of the WebApp (property.html, analytics.html, about.html, contact.html). It also contains the base.html which provides a common template for other HTML files in the project. For example, this is where the style-sheet is imported or the menu-bar is created.
### 3.5) app.py
### 3.6) dash_app.py



