from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
import simplejson as json
from api_key import api_key
from bokeh.plotting import figure, output_file, show, save
from bokeh.embed import components


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/plot_vals', methods=['GET'])
def plot_vals():
    ticker_symbol = request.args.get('ticker_symbol')
    open_ = request.args.get('Open')
    close_ = request.args.get('Close')
    adj_open = request.args.get('Adj. Open')
    adj_close = request.args.get('Adj. Close')

    url = f"https://www.quandl.com/api/v3/datasets/WIKI/{ticker_symbol}/data.json?api_key={api_key}"
    data = json.loads(requests.get(url).text)
    df = pd.DataFrame(data['dataset_data']['data'], columns=data['dataset_data']['column_names'])
    df['Date'] = pd.to_datetime(df['Date'])
    output_file("templates/lines.html")

    p = figure(title="QUANDL data", x_axis_label='Date', x_axis_type='datetime')
    plot_vals = [open_, close_, adj_open, adj_close]
    colors = {open_:'orange', close_:'green', adj_open:'blue', adj_close:'red'}
    ind = 0
    for feat in plot_vals:
        if feat is not None:
            leg = ticker_symbol.upper() + "-" + feat
            # add a line renderer with legend and line thickness
            p.line(x=df['Date'], y=df[feat], legend=leg, line_width=1, color=colors[feat])
            ind += 1
    save(p)
    # Embed plot into HTML via Flask Render
    script, div = components(p)
    return render_template('plot.html', script=script, div=div)
    # return render_template('lines.html')

if __name__ == '__main__':
    app.run(port=33507)
