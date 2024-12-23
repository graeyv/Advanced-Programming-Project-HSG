# Programming with Advanced Computer Languages Group Poject: smartprop
Determining the value of your property can be quite difficult if you don't want to pay for an expensive estimation. Our solution smartprop solves this problem in a quick and easy way using a hedonic pricing approach. 

For our project we have decided to code a prototype of a Web Application which allows Swiss homeowners to get a quick prediction of the price of their property based on its characteristics (e.g. square-meters, location, etc.) as well as a comparison to the market. The predictive model is a Random Forest, which we have trained with data that we scraped (April 2024) from [Immoscout24.ch](https://www.immoscout24.ch/en), the leading Swiss real estate market place.

Authors of this project are: 
- Yves Grädel (yves.graedel@student.unisg.ch)
- Jonas Lehmann (jonas.lehmann@student.unisg.ch)
- Marc Berger (marc.berger@student.unisg.ch)

This file provides a description of the project and is structured as follows: 
- Video demo of the Web Application 
- How to run the code
- Description of the different files

## Disclaimer
This project has been realized with the help of online sources such as https://stackoverflow.com/ and with the help of OpenAIs' LLM ChatGPT 4 (https://chatgpt.com/). Moreover, images and logos used in the WebApp have been created using AI tools such as [looka.com](https://looka.com/).

## 1) Web App Demo
Click on the image below to see the demo. Please do not share the video or the link to it.

[![Watch the video](http://img.youtube.com/vi/k0ZD0h8pN6M/0.jpg)](https://youtu.be/k0ZD0h8pN6M)

## 2) How to run the code

The code used to scrape the data (immo_crawler.py), clean the data (data_cleaning.py) and fit the predictive model (immo_random_forest.py) can be run independently from the code used to create the WebApp.

### 2.1) Web App
In order to run the WebApp you can locally download all the files in the below picture. It is IMPORTANT to keep the project files in the correct structure, otherwise paths must be adapted: 

![image](https://github.com/graeyv/Advanced-Programming-Project-HSG/assets/161760200/48aaf3a7-c5ed-4e14-a34b-1790df104efe)

The Repository is currently organized in this way. However, due to a restriction of the file sizes two placeholders (adr_data_clean_EXAMPLE.csv & best_random_forest_model_PLACEHOLDER.pkl.txt) have been added to the Repo instead of the correct files. These should be replaced and renamed accordingly (adr_data_clean.csv & best_random_forest_model.pkl):
- The correct .csv file of the Swiss addresses register can be downladed from https://www.swisstopo.admin.ch/de/amtliches-verzeichnis-der-gebaeudeadressen
- The correct .pkl file can directly be generated using the (immo_random_forest.py) script.

Moreover, it is important to download all the necessary packages which are imported at the top of the respective scripts. Once this is all done, the WebApp can be started by running the app.py script. Clicking on the link appearing in the console output will open the App in the default browser of your machine: 

![image](https://github.com/graeyv/Advanced-Programming-Project-HSG/assets/161760200/62a31850-8933-4c95-8cc1-b7985e011839)

### 2.2) Web Scraper

To scrape data from immoscout24.ch use the Scrapy spider in immo_crawler.py. The spider will crawl immoscout24.ch based on the specified filters and extract the data. Change the parameters flat_house, rent_buy, place_lvl, and place to customize the search criteria as needed. The collected data will be saved in a CSV file in the same directory. 

### 2.3) Predictive Model: Random Forest

The script immo_random_forest.py trains a Random Forest model to predict house prices based on various features. The trained model is saved as best_random_forest_model.pkl and the feature columns are saved as feature_columns.pkl for future use in the web application.

### 2.4) Data Cleaning

The data_cleaning.py script can simply be run - you just need to make sure that all files are loaded correctly. This program has a long runtime (approx. 30 minutes), but it does not necessarily have to be run, as the output file (dat_clean.csv) is also already provided.

## 3) Description of all folders/files
### 3.1) data
#### 3.1.1) adr_data_clean.csv
This is a .csv file containing the addresses of all buildings in Switzerland with the corresponding long/lat coordinates. As mentioned above the one in the repo is simply an example, the real .csv would need to run the app. The address register is mainly used to link the adresses of immoscout properties (as well as the address of the user's propery) with their corresponding long/lat coordinates to create the interactive map in the Web App. Moreover, it is used in the WebbApp to check that the address provided by the user is indeed a valid a Swiss address.
#### 3.1.2) dat_clean.csv
This is the cleaned .csv file of the scraped data from immoscout24.ch. Each observation represents one property. This data is used to (i) train the ML model and (ii) to populate the data visualizations in the WebApp. 
### 3.2) model
#### 3.2.1) best_random_forest_model.pkl
This is a pickle file which contains the trained random forest model that is loaded into the app to make a prediction of the user's property price based on his/her input. The real file must be generated using the code (immo_random_forest.py) as the file in the repo is just a placeholder. 
#### 3.2.2) feature_columns.pkl 
This pickle file simply contains the variables which are actually used to train the model. For simplicity not all scraped data has been integrated into the WebApp and the predictive model. 
### 3.3) static
This folder contains all images (.png) which are used in the WebApp such as the avatars, the logo and name of the App, as well as the picture on the 'contact us' page.
### 3.4) templates

#### 3.4.1) base.html
Defines the base template with common layout and styling using Bootstrap. Includes a navigation bar and placeholders for page-specific content.

#### 3.4.2) property.html
Extends base.html to provide a form for users to input property information, including characteristics and location details. Displays messages and pre-filled data from the backend.

#### 3.4.3) analytics.html
Extends base.html and embeds the Dash application in an iframe to display interactive data visualizations.

#### 3.4.4) contact.html
Extends base.html to provide a contact form for users to send messages to our E-mail address. Displays success messages and includes a contact-related image.

#### 3.4.5) about.html
Extends base.html to provide information about the project and team members, including a project description and team member avatars.

### 3.5) app.py
This python script initializes and configures the main Flask web application, handling routing, sessions, email functionality, data loading, and predictive modeling.

Key Functions and Features:
- Packages: Imports essential packages including Flask, Flask-Mail, Flask-Session, and custom modules.
- Initialization: Creates and configures the Flask app with session management and email settings.
- Data Loading: Loads address data and a pre-trained Random Forest model along with feature columns.
- Prediction Function: Defines a function to predict house prices based on user input.
- Routing: Sets up routes for various pages (property, analytics, about, contact) and handles form submissions and redirects.
- Email Functionality: Configures and sends emails via the contact form.
- Dash Integration: Integrates a Dash app within the Flask app for analytics visualization.

This file is essential for setting up the web application's backend, managing user sessions, rendering templates, and integrating machine learning predictions.

### 3.6) dash_app.py
This python script sets up and configures a Dash application integrated with the Flask App. It handles data visualization, interactive mapping, and data presentation for the web application.

Key Functions and Features:
- Packages: Imports necessary libraries including Dash, Dash-Leaflet for interactive maps, and Matplotlib for color mapping.
- Data Loading: Loads and preprocesses property data
- Utility Functions:
  - Translation: Translates feature names from German to English.
  - Data Processing: Calculates average values and prepares data for display.
  - Color Mapping: Generates a colormap based on property prices for visual representation on maps.
  - SVG Generation: Creates static SVG graphics for predicted price ranges.
  - Text Generation: Creates informative text based on property data.
- Dash Application:
  - Layout: Defines the layout of the Dash app including tables and maps.
  - Callbacks: Updates the data table, price range graph, and map markers based on user input and session data.

This file is essential for creating interactive and visually appealing components that display property data and analytics within the web application.

### 3.7) data_generation
#### 3.7.1) web_scraper
##### 3.7.1.1) immo_crawler.py

This Scrapy spider extracts data from immoscout24.ch based on specified filters. It accesses each listing and extracts all relevant information for all results matching the specified filters. The extracted information is stored in a .csv file.

In addition to the price and address of each listing, the spider collects all information from the "Hauptangaben" (main details) and "Eigenschaften" (features) sections. The website displays a maximum of 1,000 listings per search query, so for large cantons with many listings, multiple queries may be required. The crawler could be further improved to handle this limitation.

The crawler is configured to respect robots.txt and includes a download delay to avoid being blocked by the website.

#### 3.7.2) data_cleaning
##### 3.7.2.1) data_cleaning.py

This Python file is used to clean the raw data from the web_scraper. 

All files were first loaded from the “raw_data_immoscout” folder and then checked for correctness and completeness. In the course of the process, assumptions had to be made as the data did not exactly match the data on the website - the documentation of these assumptions can also be found in this file. Additionally, information that was not required was removed and new information that was important for the model was included from other sources (see folder “additional_data”). 

The output of this file is the dat_clean.csv. file, which was used both for the model and for the dash_app. 

##### 3.7.2.2) dat_clean.csv

This is the output file of the data cleanings and serves as the base for the model and the dash_app. In short, this data includes all addresses, prices, living areas, property ages, region types and other features of the apartments. 

##### 3.7.2.3) raw_data_immoscout

This folder contains the raw data from the web_scraper. It consists of 59 different csv. files, which are divided according to canton and type of search. Due to restrictions on scraping we had to perform it chunkwise, which explains why we have many different files.

##### 3.7.2.4) additional_data

This folder contains all additional data that was used in addition to the data originating from the web_scraper. The data was used to check the correctness of the addresses and provided information regarding the categorization of the ZIPs into a location category. 

### 3.8) immo_random_forest.py

The script trains a Random Forest model to predict housing prices using the data scraped from immoscout24.ch. It employs RandomizedSearchCV to optimize the hyperparameters for the Random Forest Regressor.

The predictor variables used in the model are: 'living_area', 'Balkon', 'Garage', 'Parkplatz', 'Neubau', 'Swimmingpool', 'Lift', 'Aussicht', 'Cheminée', 'Rollstuhlgängig', 'Kinderfreundlich', 'Kabel-TV', 'Minergie Bauweise', 'Minergie zertifiziert', 'PLZ_only'.

To simplify user input, other available variables in the scraped data are not used.

When evaluating the model on a test set, it achieves a mean absolute error (MAE) of approximately CHF 250,000 and an R² value of 0.6.




