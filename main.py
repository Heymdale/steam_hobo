import platform


def main():
    os = platform.system()
    match os:
        case "Windows":
            from main_win import main_os
            main()
        case "Linux":
            from main_lin import main_os
        case _:
            print("Unsupported OS")
            exit()
    main_os()


if __name__ == '__main__':
    main()
