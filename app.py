# packages
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_mail import Mail, Message
from flask_session import Session
from datetime import timedelta
from dash_app import create_dash_app
import os
import pandas as pd
import joblib

#################################################### MISC: FLASK SESSION, LOADING DATA, LOADING PREDICTIVE MODEL, EMAIL EXTENSION, DEFINE FUNCTIONS ########################################################

# initialize web application
app = Flask(__name__)
app.secret_key = 'supersecretkey1234567890'

# Configure Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'  # Store session data in filesystem
app.config['SESSION_PERMANENT'] = False  # Sessions are non-permanent
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=45)  # Adjust the session lifetime as needed
Session(app)  # Initialize Flask-Session

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'adv.prog.project@gmail.com'
app.config['MAIL_PASSWORD'] = 'rrir esvm txfz dbli'  # App-specific password

# initialize mail extension
mail = Mail(app)

# globally load the addresses data
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, 'data', 'adr_data_clean.csv')
# efficient load
adr_data_clean = pd.read_csv(data_path, delimiter=';', usecols=['ADR_NUMBER', 'zip', 'place', 'STN_LABEL', 'long', 'lat'], dtype={'zip': str, 'ADR_NUMBER': str})
# normalize to avoid case sensitive comparisons
adr_data_clean['place'] = adr_data_clean['place'].str.lower()
adr_data_clean['STN_LABEL'] = adr_data_clean['STN_LABEL'].str.lower()

# load the predictive model as well as feature cols
model_path = os.path.join(script_dir, 'model', 'best_random_forest_model.pkl')
cols_path = os.path.join(script_dir, 'model', 'feature_columns.pkl')
model = joblib.load(model_path)
feature_columns = joblib.load(cols_path)

# define function to predict house price
def predict_price(input_data, feature_columns, model): 
    # convert input to df
    input_df = pd.DataFrame([input_data])
    # ensure all cols are present
    for col in feature_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    # ensure that user input has order matching training data
    input_df = input_df[feature_columns]
    # make prediction
    prediction = model.predict(input_df)
    # result
    return prediction[0]

########################################################################## ROUTES FOR DIFFERENT PAGES OF WEBAPP #####################################################################################

# Redirect root URL to the Property Page
@app.route('/')
def root():
    return redirect(url_for('property'))

# Route for the Property Page
@app.route('/property', methods=['GET', 'POST'])
def property():
    data = {}
    message = ""

    if request.method == 'POST':
        
        # Collect and process all form data
        data['living_area'] = request.form['living_area']
        data['construction_year'] = request.form['construction_year']
        data['Balkon'] = request.form['Balkon']
        data['Garage'] = request.form['Garage']
        data['Parkplatz'] = request.form['Parkplatz']
        data['Neubau'] = request.form['Neubau']
        data['Swimmingpool'] = request.form['Swimmingpool']
        data['Lift'] = request.form['Lift']
        data['Aussicht'] = request.form['Aussicht']
        data['Cheminée'] = request.form['Cheminée']
        data['Rollstuhlgängig'] = request.form['Rollstuhlgängig']
        data['Kinderfreundlich'] = request.form['Kinderfreundlich']
        data['Kabel-TV'] = request.form['Kabel-TV']
        data['Minergie Bauweise'] = request.form['Minergie Bauweise']
        data['Minergie zertifiziert'] = request.form['Minergie zertifiziert']
        data['PLZ_only'] = request.form['PLZ_only'].strip()  # Strip whitespace
        data['place'] = request.form['place'].strip().lower()  # Strip whitespace and lowercase
        data['street'] = request.form['street'].strip().lower()  # Strip whitespace and lowercase
        data['nr'] = request.form['nr'].strip()  # Strip whitespace

        # Treat the Zip separately because it is categorical (one hot encoded)
        user_zip = data['PLZ_only']

        # Initialize input data dictionary with zeros
        input_data = {col: 0 for col in feature_columns}

        # update input_data with actual values
        input_data.update({
            'living_area': data['living_area'],
            'Balkon': 1 if request.form['Balkon'] == 'Yes' else 0,
            'Garage': 1 if request.form['Garage'] == 'Yes' else 0,
            'Parkplatz': 1 if request.form['Parkplatz'] == 'Yes' else 0,
            'Neubau': 1 if request.form['Neubau'] == 'Yes' else 0,
            'Swimmingpool': 1 if request.form['Swimmingpool'] == 'Yes' else 0,
            'Lift': 1 if request.form['Lift'] == 'Yes' else 0,
            'Aussicht': 1 if request.form['Aussicht'] == 'Yes' else 0,
            'Cheminée': 1 if request.form['Cheminée'] == 'Yes' else 0,
            'Rollstuhlgängig': 1 if request.form['Rollstuhlgängig'] == 'Yes' else 0,
            'Kinderfreundlich': 1 if request.form['Kinderfreundlich'] == 'Yes' else 0,
            'Kabel-TV': 1 if request.form['Kabel-TV'] == 'Yes' else 0,
            'Minergie Bauweise': 1 if request.form['Minergie Bauweise'] == 'Yes' else 0,
            'Minergie zertifiziert': 1 if request.form['Minergie zertifiziert'] == 'Yes' else 0
        })
        
        # Transform the user-entered zip code into the appropriate one-hot encoding
        zip_column = f'PLZ_only_{user_zip}'
        if zip_column in feature_columns:
            input_data[zip_column] = 1
        
        # Ensure all one-hot encoded columns are included and set to 0 if not present in input data
        for col in feature_columns:
            if col not in input_data:
                input_data[col] = 0

        # check model input
        print(input_data)
        
        # prediction
        predicted_price = predict_price(input_data, feature_columns, model)
        data['predicted_price'] = round(predicted_price, 0)
        data['price_lower'] = round(predicted_price * 0.9, 0)
        data['price_upper'] = round(predicted_price * 1.1, 0)
        

        # Check if the address is valid using direct filtering
        matching_address = adr_data_clean[
            (adr_data_clean['zip'] == data['PLZ_only']) &
            (adr_data_clean['place'] == data['place']) &
            (adr_data_clean['STN_LABEL'] == data['street']) &
            (adr_data_clean['ADR_NUMBER'] == data['nr'])
        ]

        if not matching_address.empty:
            # Address is valid, retrieve longitude and latitude
            data['long'] = matching_address.iloc[0]['long']
            data['lat'] = matching_address.iloc[0]['lat']
            
            # Store data in session
            session['property_data'] = data
            message = "Information Saved!"
        else:
            # Address is incorrect
            message = "Invalid address. Please check the details and try again."

    return render_template('property.html', data=data, message=message)

# initialize dash app
dash_app = create_dash_app(app)

# Route for the Analytics Page
@app.route('/analytics')
def analytics():
    # check if property_data provided by user is present in session
    if "property_data" not in session: 
        # redirect user to property page
        return redirect(url_for('property'))
    
    return render_template('analytics.html')

# Route for Dash app
@app.route('/dash_analytics')
def analytics_iframe():
    return dash_app.index()

# Route for the About Page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for the Contact Page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message_body = request.form['message']

        # Create the message
        msg = Message(
            subject=subject,
            sender=('Property WebApp', 'your_gmail_username@gmail.com'),
            recipients=['adv.prog.project@gmail.com'],
            body=f"Message from {name} ({email}):\n\n{message_body}"
        )

        # Send the message
        mail.send(msg)
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
