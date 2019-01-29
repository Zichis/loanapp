import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


class RandomForestAlgorithm:
    def __init__(self, annual_income, purpose, home_ownership, term, length_of_employment, time_of_employment, dti, percentage_available_credit, borrower_deliquency, total_late_fees):
      self.annual_income = annual_income
      self.purpose = purpose
      self.home_ownership = home_ownership
      self.term = term
      self.length_of_employment = length_of_employment
      self.time_of_employment = time_of_employment
      self.dti = dti
      self.percentage_available_credit = percentage_available_credit
      self.borrower_deliquency = borrower_deliquency
      self.total_late_fees = total_late_fees

    def process(self):
      loan_data = pd.read_csv('final_loan_data.csv', index_col=0)

      # Separating target variables
      X = loan_data.values[:, :9]
      Y = loan_data.values[:, 9]

      # Splitting train and test data

      X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=100)

      # Creating a random forest classifier
      clf = RandomForestClassifier(random_state=0)

      # Training the classifier
      clf.fit(X_train, y_train)

      input_data = [
          # self.annual_income,
          self.purpose,
          self.time_of_employment,
          self.length_of_employment,
          self.home_ownership,
          self.dti,
          self.term,
          self.borrower_deliquency,
          self.percentage_available_credit,
          self.total_late_fees
      ]

      # Predict
      # prediction = clf.predict(X_test)

      prediction = clf.predict([input_data])

      if prediction[0] == 1:
          prediction = "Eligible"
      else:
          prediction = "Not eligible"

      return prediction
