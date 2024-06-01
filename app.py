from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    url = request.form['url']
    results = scan_for_vulnerabilities(url)
    return render_template('results.html', url=url, results=results)

def scan_for_vulnerabilities(url):
    # Simple SQL Injection test
    payloads = ["'", "' OR '1'='1", "' OR '1'='1' -- "]
    results = []
    for payload in payloads:
        test_url = f"{url}{payload}"
        response = requests.get(test_url)
        if "error" in response.text or "SQL" in response.text:
            results.append(f"SQL Injection vulnerability detected with payload: {payload}")
    if not results:
        results.append("No SQL Injection vulnerabilities detected.")
    return results

if __name__ == '__main__':
    app.run(debug=True)
