from flask import *
import pandas as pd
from flask import Flask, request, jsonify
import spacy

app = Flask(__name__)
df = pd.read_csv(r"F:\DS\task2\sales_data_sample.csv", encoding='unicode_escape')
months = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
df['MONTH_NAME'] = df['MONTH_ID'].map(months)
@app.route('/')
def home():
  return "<h2> Hi <h2>"

@app.route('/contact')
def contact():
  return "<h2> Kowshik </h2>"
@app.route('/query_example')
def query_example():
  query = request.args.get('query')

  return '''<h1> The Query is : {}</h1>'''.format(query)
@app.route('/form_example',methods=['POST','GET'])
def form_example():
  if request.method == 'POST':
    query = request.form.get('query')
    return '<h1> Submitted data is {}.</h1>'.format(query)
  return '''<form method='POST'> Query <input type = 'text' name = 'query'>
  <input type='submit'>
  </form>
  '''
@app.route('/json_example',methods=['POST'])
def json_example():
    req_data = request.get_json()
    query = req_data['query'][2]
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(query)

    # Extracting relevant information from the query
    item = None
    city = None
    month = None

    months = ['January', 'February','March','April','May','June','July','August','September','October','November','December']
    for token in doc:
        if token.dep_ == "dobj" and token.head.pos_ == "VERB" and token.head.text == "earning":
            item = token.text
        elif token.dep_ == "nsubj" and token.head.pos_ == "VERB" and token.head.text == "city":
            city = token.text
        elif token.dep_ == "pobj" and token.head.pos_ == "ADP" and token.head.text == "in":
            month = token.text

    # Retrieving the required data from the DataFrame
    if 'top earning sale item' in query:
        top_item = df.groupby('PRODUCTLINE').sum()['SALES'].sort_values(ascending=False).keys()[0]
        answer = f"The top earning sale item is {top_item}."
    elif 'city has my best sales' in query:
        best_city = df.groupby("CITY").sum()["SALES"].sort_values(ascending=False).index[0]
        answer = f"The city with the best sales is {best_city}."
    elif 'January February March April May June July August September October November December' in query:
        month_name = [word for word in query.split() if word in months]

        # Converting the month to a datetime object
        # month = pd.to_datetime(month, format="%B").month

        # Filtering the DataFrame by month
        monthly_sales = df[df["MONTH_NAME"] == month]["SALES"].sum()
        avg_monthly_sales = df.groupby(df["MONTH_NAME"]).mean()["SALES"][month]
        if monthly_sales > avg_monthly_sales:
            answer = f"There is a trend happening in {month} with higher sales than average."
        else:
            answer = f"There is an anomaly in {month} with lower sales than average."
    else:
        answer = "Sorry, I didn't understand the question."

    # Returning the answer
    # return jsonify({"answer": answer})
    return '''<h1> The answer is : {} </h1>'''.format(answer)

if __name__ == '__main__':
    app.run(debug=True,port=2000)