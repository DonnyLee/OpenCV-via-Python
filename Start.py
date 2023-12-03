from prog import Webcam, Terminal


def main():
    w = Webcam.Webcam()
    w.stream_on_window()


if __name__ == "__main__":
    # execute only if run as a script
    main()