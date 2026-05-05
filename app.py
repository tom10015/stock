from flask import Flask, jsonify, request
import requests
import time

app = Flask(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_yahoo_options(symbol):
    url = f"https://query2.finance.yahoo.com/v7/finance/options/{symbol}"
    r = requests.get(url, headers=HEADERS)
    data = r.json()

    result = data["optionChain"]["result"][0]
    quote = result["quote"]
    options = result["options"][0]

    stock_price = quote.get("regularMarketPrice", None)
    exp_date = options.get("expirationDate", None)

    calls = options.get("calls", [])

    # Find best covered call (highest bid premium)
    best = None
    for call in calls:
        bid = call.get("bid", 0)
        if best is None or bid > best.get("bid", 0):
            best = call

    if best is None:
        return None

    return {
        "symbol": symbol.upper(),
        "stockPrice": stock_price,
        "expirationDate": time.strftime('%Y-%m-%d', time.gmtime(exp_date)),
        "strike": best.get("strike"),
        "bid": best.get("bid"),
        "lastPrice": best.get("lastPrice"),
        "volume": best.get("volume"),
        "openInterest": best.get("openInterest")
    }

@app.route("/api/coveredcall", methods=["GET"])
def covered_call():
    symbol = request.args.get("symbol", "")
    if not symbol:
        return jsonify({"error": "symbol is required"}), 400

    try:
        data = get_yahoo_options(symbol)
        if data is None:
            return jsonify({"error": "No option chain data found"}), 404
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/top", methods=["POST"])
def top_list():
    symbols = request.json.get("symbols", [])
    results = []

    for sym in symbols[:100]:
        try:
            data = get_yahoo_options(sym)
            if data:
                results.append(data)
        except:
            continue

    # Sort by bid premium highest
    results.sort(key=lambda x: (x["bid"] if x["bid"] else 0), reverse=True)

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
