from ewmh import EWMH
import config


def test_ewmh_wrapper(name, ewmh_func):
    ewmh = EWMH()
    windows = ewmh.getClientList()
    find_windows = []
    for el in windows:
        w_name = ewmh.getWmName(el)
        if w_name is not None:
            if -1 != w_name.decode('utf-8').find(name):
                find_windows.append(el)
                break
    if len(find_windows) > 0:
        print(ewmh.getWmName(find_windows[0]).decode('utf-8'))
        ewmh_func(find_windows[0])  # В данной версии запускаем по одному экземпляру, коллизии не обрабатываем
        ewmh.display.flush()
        return find_windows[0]
    else:
        print('Something get wrong')


ewmh = EWMH()
windows = ewmh.getClientList()
name = config.warning_headline
win = test_ewmh_wrapper(name, ewmh.setCloseWindow)
# ewmh.setCloseWindow(win)
# ewmh.display.flush()

# ewmh.setCloseWindow(starve_windows[0])
# ewmh.display.flush()
# main.dontstarve_control()
