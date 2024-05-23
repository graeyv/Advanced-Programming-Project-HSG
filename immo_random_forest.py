# packages
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from scipy.stats import randint
import joblib

# Read data
data = pd.read_csv('dat_clean.csv')

# Filter the DataFrame to keep only the specified columns
columns_to_keep = [
    'living_area', 'Balkon', 'Garage', 'Parkplatz', 'Neubau', 
    'Swimmingpool', 'Lift', 'Aussicht', 'Cheminée', 'Rollstuhlgängig', 
    'Kinderfreundlich', 'Kabel-TV', 'Minergie Bauweise', 
    'Minergie zertifiziert', 'PLZ_only', 'price'
]

data = data[columns_to_keep]

# Convert 'PLZ_only' to string
data['PLZ_only'] = data['PLZ_only'].astype(str)

# One-hot encode 'PLZ_only' and other categorical variables
data_encoded = pd.get_dummies(data, columns=['PLZ_only'], drop_first=True)

# Prepare the feature set (X) and target variable (y)
X = data_encoded.drop(columns=['price'])
y = data_encoded['price']

# Split the data into training and testing sets (80-20 split)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest Regressor
random_forest_model = RandomForestRegressor(random_state=42)

# Define the parameter distribution for RandomizedSearchCV
param_dist = {
    'n_estimators': randint(50, 200), 
    'max_depth': [None, 10, 20], 
    'min_samples_split': randint(2, 10),
    'min_samples_leaf': randint(1, 4),
    'bootstrap': [True, False]
}

# Initialize RandomizedSearchCV
random_search = RandomizedSearchCV(estimator=random_forest_model, param_distributions=param_dist, n_iter=20, cv=3, n_jobs=-1, scoring='neg_mean_absolute_error', random_state=42)

# Fit the model to the training data
random_search.fit(X_train, y_train)

# Get the best model from RandomizedSearchCV
best_rf_model = random_search.best_estimator_

# Save the best model
joblib.dump(best_rf_model, 'best_random_forest_model.pkl')

# Save the feature columns
joblib.dump(X_train.columns.tolist(), 'feature_columns.pkl')

# Make predictions on the test set
rf_preds = best_rf_model.predict(X_test)

# Evaluate the model
mae = mean_absolute_error(y_test, rf_preds)
r2 = r2_score(y_test, rf_preds)

# Display the results
print(f"Best Parameters: {random_search.best_params_}")
print(f"Mean Absolute Error: {mae}")
print(f"R² Score: {r2}")