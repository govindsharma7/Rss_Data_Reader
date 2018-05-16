from flask import Flask,render_template,request,jsonify
import os
import json
from datetime import datetime ,timedelta
import sys
import linecache
import urllib.request as urllib2
import xmltodict

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

# API

@app.route('/api/v1/rss/getdata', methods=['POST'])
def rss_post():
	try:
		data_collection = ""
		file = urllib2.urlopen(request.json['rss_url'])
		data = file.read()
		file.close()
		data = xmltodict.parse(data)
		if len(data['rss']['channel']['item']) > 0:
			for all_collection in data['rss']['channel']['item']:
				d_date = datetime.strptime(all_collection['pubDate'],"%a, %d %b %Y %H:%M:%S %Z")
				data_collection += '''
					<div class="container post_div">
						<p><b><a href="'''+all_collection['link']+'''">'''+all_collection['title']+'''</a></b><small>&nbsp; '''+str(d_date.date().strftime('%b %d, %Y'))+'''</small></p>
						<p>'''+all_collection['description']+'''</p>
					</div>
					<div class="clearfix"></div>
					'''
			return jsonify({'status':200 , 'message' : 'success' , 'rss_data' : data_collection})
		else:
			return jsonify({'status':204 , 'message' : 'No Record Found' , 'rss_data' : data_collection})
	except Exception as e:
		PrintException()

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

app.secret_key = os.urandom(24)

if __name__== "__main__":
    app.run(host='0.0.0.0',port=5001,debug=True,threaded=True)
