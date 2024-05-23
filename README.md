# Programming with Advanced Computer Languages Group Poject: smartprop
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
This project has been realized with the help of online sources such as https://stackoverflow.com/ and with the help of OpenAIs' LLM ChatGPT 4 (https://chatgpt.com/). Moreover, images and logos used in the WebApp have been created using AI tools such as [looka.com](https://looka.com/)).

## 1) Web App Demo
Click on the image below to see the demo. Please do not share the video or the link to it.

[![Watch the video](http://img.youtube.com/vi/k0ZD0h8pN6M/0.jpg)](https://youtu.be/k0ZD0h8pN6M)

## 2) How to run the code

The code used to scrape the data (NAME), clean the data (NAME) and fit the predictive model (NAME) can be run independently from the code used to create the WebApp.

### 2.1) Web App
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

## 3) Description of all folders/files
### 3.1) data
#### 3.1.1) adr_data_clean.csv
This is a .csv file containing the addresses of all buildings in Switzerland with the corresponding long/lat coordinates. As mentioned above the one in the repo is simply an example, the real .csv would need to run the app. The address register is mainly used to link the adresses of immoscout properties (as well as the address of the user's propery) with their corresponding long/lat coordinates to create the interactive map. Moreover, it is used in the WebbApp to check that the address provided by the user is indeed a valid a Swiss address.
#### 3.1.2) dat_clean.csv
This is the cleaned .csv file of the scraped data from immoscout24.ch. Each observation represents one property. (MAYBE SHORT DESCRIPTION OF VARS?). This data is used to (i) train the ML model and (ii) to populate the data visualizations in the WebApp. 
### 3.2) model
#### 3.2.1) best_random_forest_model.pkl
This is a pickle file which contains the trained random forest model that is loaded into the app to make a prediction of the user's property price based on his/her input. The real file must be generated using the code (NAME) as the file in the repo is just a placeholder. 
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

### 3.7) Etc.



