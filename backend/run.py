from dotenv import load_dotenv
load_dotenv()


def main():
    """
    Start backend

    :return: None
    """
    import app
    from config import Development
    app = app.create(Development)
    app.run()


if __name__ == "__main__":
    main()
