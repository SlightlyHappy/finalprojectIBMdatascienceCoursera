import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period='max')
tesla_data.reset_index(inplace=True)
print(tesla_data.head(5))

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
response = requests.get(url)
html_data = response.text

soup = BeautifulSoup(html_data, "html.parser")
table = soup.find_all("table")[1]
rows = table.find_all("tr")
dates = []
revenues = []
for row in rows[1:]:
    cells = row.find_all("td")
    date = cells[0].text
    revenue = cells[1].text.replace(",", "").replace("$", "")
    dates.append(date)
    revenues.append(revenue)

tesla_revenue = pd.DataFrame({"Date": dates, "Revenue": revenues})

tesla_revenue["Revenue"] = pd.to_numeric(tesla_revenue["Revenue"])

print(tesla_revenue.tail())

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing=0.3)

    stock_data_specific = stock_data[stock_data["Date"] <= '2021-06-14']
    revenue_data["Date"] = pd.to_datetime(revenue_data["Date"])  # Convert "Date" column to datetime
    revenue_data_specific = revenue_data[revenue_data["Date"] <= '2021-04-30']

    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific["Date"], infer_datetime_format=True), y=stock_data_specific["Close"].astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=revenue_data_specific["Date"], y=revenue_data_specific["Revenue"].astype("float"), name="Revenue"), row=2, col=1)

    fig.update_layout(showlegend=False, title_text=f"{stock} Stock Data and Revenue")
    fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue (Millions)", row=2, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)

    fig.show()

make_graph(tesla_data, tesla_revenue, "Tesla")




gme = yf.Ticker("GME")
gme_data = gme.history(period="max")
gme_data.reset_index(inplace=True)
print(gme_data.head())

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
response1 = requests.get(url)
html_data1 = response1.text

soup = BeautifulSoup(html_data1, "html.parser")

table = soup.find_all("table")[2]
rows = table.find_all("tr")

dates = []
revenues = []

for row in rows[1:]:
    cells = row.find_all("td")
    if len(cells) == 2:
        date = cells[0].text
        revenue = cells[1].text.replace(",", "").replace("$", "")
        dates.append(date)
        revenues.append(revenue)

gme_revenue = pd.DataFrame({"Date": dates, "Revenue": revenues})


gme_revenue["Revenue"] = pd.to_numeric(gme_revenue["Revenue"])


print(gme_revenue.tail())


make_graph(gme_data, gme_revenue, "GameStop")

