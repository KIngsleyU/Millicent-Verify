# Millicent-Verify

## Chrome extension with server-side sklearn (example)

This repo now includes a small demo showing how to keep machine learning on the server (Python + scikit-learn) and call it from a Chrome extension.

### Files
- `slope_server.py` — Flask server; fits a simple LinearRegression on x = [1, 2, 3] and user-provided y values, returns the slope.
- `sklearn_ext/` — Chrome extension (MV3) with a popup form that POSTs the three numbers to the local server and displays the slope.

### Run the server (Python)
```bash
pip install flask scikit-learn numpy
python slope_server.py  # serves http://localhost:5000
```

### Load the extension (Chrome)
1. Visit `chrome://extensions`, enable Developer mode.
2. Click “Load unpacked” and choose `sklearn_ext/`.
3. In the popup, enter three numbers; it will call the server and show the slope.