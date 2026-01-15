def start_extension():
    # RapydScript maps this Pythonic code to JavaScript.
    msg = "Hello from RapydScript (Python -> JS)!"
    alert(msg)  # alert is a browser global that RapydScript will emit as JS
    print(alert(msg))

start_extension()