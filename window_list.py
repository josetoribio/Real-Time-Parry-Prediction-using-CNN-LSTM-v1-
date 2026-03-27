import pygetwindow as gw

windows = gw.getAllTitles()
for w in windows:
    if w.strip():  # ignore empty titles
        print(repr(w))