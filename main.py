# create flask api movie with /search /get/<base64>
import os,base64,json
from flask import Flask, request, jsonify,render_template
from flask_cors import CORS

from providers import Provider


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    providers = Provider().listProviders()
    return render_template('index.html',providers=providers)

@app.route('/detail')
def detail():
    _detail = request.args.get("detail")
    _decode = base64.b64decode(_detail.encode()).decode("utf-8")
    _json = json.loads(_decode)
    link = _json["link"]
    provider = _json["provider"]
    if not link:
        return jsonify({"error": "link not found"})
    result = Provider().get(link,provider)
    return render_template('detail.html',data=result)

@app.route('/detail-series')
def detailSeries():
    _detail = request.args.get("detail")
    _decode = base64.b64decode(_detail.encode()).decode("utf-8")
    _json = json.loads(_decode)
    link = _json["link"]
    provider = _json["provider"]
    if not link:
        return jsonify({"error": "link not found"})
    result = Provider().get(link,provider)
    return render_template('detail-series.html',data=result)

@app.route("/api/providers")
def providers():
    return jsonify(Provider().listProviders()),200

@app.route("/api/search")
def search():
    query = request.args.get("query")
    providers = request.args.getlist("providers[]",None)
    page = request.args.get("page",1)
    if not query:
        return jsonify({"error": "query not found"})
    result = Provider().search(query=query,providers=providers,page=page)
    return jsonify(result),200

@app.route("/api/get")
def get():
    link = request.args.get("link")
    provider = request.args.get("provider")
    if not link:
        return jsonify({"error": "link not found"})
    if not provider:
        return jsonify({"error": "provider not found"})
    result = Provider().get(link,provider)
    return jsonify(result),200

@app.route('/iframe')
def iframe():
    link = request.args.get("link")
    link = base64.b64decode(link.encode()).decode("utf-8")
    provider = request.args.get("provider",None)
    _p = Provider().findProvider(provider)
    return render_template('iframe.html',link=link,sandbox=_p.sandbox)

if __name__ == '__main__':
    config = {
        'host': '0.0.0.0',
        'port': os.getenv("PORT", default=5001),
        'debug': True
    }

    app.run(**config)