# Millicent-Verify

A collection of Chrome extension examples demonstrating different ways to use Python in browser extensions.

## Project Structure

### Extensions

1. **`simple_ext/`** - Python-to-JavaScript transpilation example
   - Uses **Transcrypt** to transpile Python code (`logic.py`) into JavaScript
   - Generated extension files are in `simple_ext/`
   - Built via `build_extension.py`

2. **`sklearn_ext/`** - Server-side machine learning example
   - Demonstrates keeping scikit-learn on the server (can't run in browser)
   - Chrome extension calls a local Flask API
   - Shows HTTP communication between extension and Python backend

### Core Files

- `build_extension.py` - Builds the Transcrypt-based extension (`simple_ext/`)
- `logic.py` - Python source code that gets transpiled to JavaScript (for `simple_ext/`)
- `slope_server.py` - Flask server that computes slopes using scikit-learn (for `sklearn_ext/`)
- `main.py` - (currently empty)

## Example 1: Python-to-JavaScript Transpilation (Transcrypt)

### How it works
- Write your logic in Python (`logic.py`)
- Transcrypt transpiles it to JavaScript
- Chrome extension runs the JavaScript

### Setup
```bash
pip install transcrypt
python build_extension.py  # Generates simple_ext/
```

### Load Extension
1. Go to `chrome://extensions`
2. Enable "Developer mode"
3. Click "Load unpacked" and select the `simple_ext/` folder
4. Visit any webpage - the extension runs on all pages

### Modify Logic
- Edit `logic.py` with your Python code
- Run `python build_extension.py` again to rebuild
- Reload the extension in Chrome

## Example 2: Server-Side ML (Flask + scikit-learn)

### How it works
- scikit-learn **cannot** run in the browser (needs NumPy/C extensions)
- Solution: Keep ML on the server, extension makes HTTP requests
- Flask server receives 3 numbers, computes slope via LinearRegression, returns result

### Setup

1. **Install dependencies:**
```bash
pip install flask flask-cors scikit-learn numpy
```

2. **Start the server:**
```bash
python slope_server.py
```
Server runs on `http://localhost:5050` (port 5050 avoids macOS AirPlay conflicts)

3. **Load the extension:**
   - Go to `chrome://extensions`
   - Enable "Developer mode"
   - Click "Load unpacked" and select `sklearn_ext/`
   - Click the extension icon to open the popup

4. **Use it:**
   - Enter 3 numbers (y values)
   - Click "Compute slope"
   - Extension POSTs to server, receives slope, displays it

### Testing the Server

Test the API directly:
```bash
curl -X POST http://localhost:5050/slope \
  -H "Content-Type: application/json" \
  -d '{"y":[1,2,2]}'
```

Expected response: `{"slope":0.5}`

### Why This Approach?

- **scikit-learn requires NumPy/SciPy** - These are C extensions that don't work in browsers
- **Transcrypt only supports pure Python subset** - Can't transpile scientific libraries
- **Solution**: Run ML server-side, extension just sends/receives data via HTTP

## Key Learnings

1. **Pure Python code** can be transpiled to JS (Transcrypt)
2. **Heavy libraries** (scikit-learn, NumPy, etc.) must stay on the server
3. **HTTP API** bridges extension (client) and Python backend (server)
4. **CORS** must be enabled on Flask server for extension to call it
