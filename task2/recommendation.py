import pandas as pd
from flask import Flask, request

# Read CSV file into a pandas dataframe
df = pd.read_csv(r'F:\DS\task2/sales_data_sample.csv', encoding='unicode_escape')
months = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
df['MONTH_NAME'] = df['MONTH_ID'].map(months)

app = Flask(__name__)


@app.route('/recommendation', methods=['POST'])
def recommendation():
    req_data = request.get_json()
    # Filter the dataframe to only include the data for the given month
    #monthly_data = df[df['Order Date'].str.startswith(month)]

    # Calculate the average sales for the month
    month = req_data["MONTH_NAME"][2]
    avg_sales = df[df['MONTH_NAME']==month]['SALES'].mean()

    # Calculate the standard deviation of the sales for the month
    std_sales = df[df['MONTH_NAME']==month]['SALES'].std()

    # Check if the average sales are significantly different from the overall average sales
    if avg_sales > df['SALES'].mean() + std_sales:
        recommendation = f"The sales for {month} are significantly higher than the overall average."
    elif avg_sales < df['SALES'].mean() - std_sales:
        recommendation = f"The sales for {month} are significantly lower than the overall average."
    else:
        recommendation = f"The sales for {month} are consistent with the overall average."

    return recommendation


if __name__ == '__main__':
    app.run(debug=True, port=3000)
