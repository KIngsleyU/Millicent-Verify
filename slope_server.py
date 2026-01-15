"""
Tiny Flask server that computes a slope using scikit-learn.

X is fixed: [1, 2, 3]
Y comes from the client: three numbers supplied by the extension.
We fit a simple LinearRegression and return the slope (gradient).
"""

import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from sklearn.linear_model import LinearRegression
import numpy as np

app = Flask(__name__)
CORS(app)  # allow extension (and localhost) to call the API


@app.post("/slope")
def slope():
    """Compute slope given three y values."""
    data = request.get_json(force=True, silent=True) or {}
    print("data: ", data)
    y = data.get("y")

    if not isinstance(y, list) or len(y) != 3:
        return jsonify(error="Send exactly 3 numbers in y"), 400

    try:
        y_vals = np.array(y, dtype=float)
    except Exception:
        return jsonify(error="All values must be numbers"), 400

    X = np.array([[1], [2], [3]], dtype=float)
    model = LinearRegression().fit(X, y_vals)
    slope_value = float(model.coef_[0])

    return jsonify(slope=slope_value)


if __name__ == "__main__":
    # Use 5050 by default to avoid macOS AirPlay/AirTunes on port 5000.
    port = int(os.environ.get("PORT", "5050"))
    app.run(port=port, debug=True)

