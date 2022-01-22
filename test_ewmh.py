from ewmh import EWMH


ewmh = EWMH()
windows = ewmh.getClientList()
starve_find_name = 'steamlibrary'
starve_windows = []
for el in windows:
    if ewmh.getWmName(el).decode('utf-8').lower().find(starve_find_name) != -1:
        starve_windows.append(el)
ewmh.setActiveWindow(starve_windows[0])
ewmh.display.flush()


