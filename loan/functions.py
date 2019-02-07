def modify_home_ownership(numerical_value):
  values = {"1":"Rent", "2":"Own", "3":"Mortgage", "4":"Other"}

  for key in values:
    if numerical_value == key:
      return values[key]

def modify_term(numerical_value):
  values = {"36":"36 months", "60":"60 months"}

  for key in values:
    if numerical_value == key:
      return values[key]

def modify_purpose(numerical_value):
  values = {
    "1":"Credit card", 
    "2":"Car", 
    "3":"Small business", 
    "4":"Other", 
    "5":"Wedding", 
    "6":"Debt consolidation", 
    "7":"Home improvement", 
    "8":"Major purchase", 
    "9":"Medical", 
    "10":"Moving", 
    "11":"Vacation", 
    "12":"House"
  }

  for key in values:
    if numerical_value == key:
      return values[key]

def modify_time_of_employment(numerical_value):
  values = {"0":"Less than a year", "1":"A year and above"}

  for key in values:
    if numerical_value == key:
      return values[key]