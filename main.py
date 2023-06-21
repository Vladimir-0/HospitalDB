from src import HospitalDB, HospitalApp


def main() -> None:
    """
    Запускает приложение для работы с HospitalDB.
    """
    db = HospitalDB("postgres", "root", "localhost", "5432", "hospital")
    app = HospitalApp(db)
    app.run()


if __name__ == '__main__':
    main()
