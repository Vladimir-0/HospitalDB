from typing import Any, Union

from sqlalchemy import create_engine, text, Engine, Result, URL, Executable
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.decl_api import DeclarativeMeta


class HospitalDB:
    def __init__(self, user: str, password: str, host: str, port: Union[str, int], db_name: str) -> None:
        """
        Программа для подключения к базе данных.
        :param user: Имя пользователя.
        :param password: Пароль.
        :param host: Адрес сервера.
        :param port: Порт сервера.
        :param db_name: Название базы данных.
        """
        # Создаём строку подключения
        url = URL.create(
            drivername="postgresql+psycopg2",
            host=host,
            port=int(port),
            username=user,
            password=password,
            database=db_name)
        # Создает движок для подключения к базе данных
        self._engine: Engine = create_engine(url)
        # Создает сессию для работы с базой данных
        self._session: Session = sessionmaker(bind=self._engine)()
        # Создает базовый класс для моделей
        self._base: DeclarativeMeta = automap_base()
        # Загружает модели из базы данных
        self._base.prepare(self._engine, reflect=True)

        # Для быстрого доступа к моделям
        self.Orders: DeclarativeMeta = self._base.classes.orders
        self.Groups: DeclarativeMeta = self._base.classes.groups
        self.Analyses: DeclarativeMeta = self._base.classes.analyses

    # Выполняет SQL-запрос, переданный в качестве аргумента
    def execute(self, query: Union[str, Executable]) -> Result[Any]:
        """
        Выполняет переданную команду команду.
        :param query: SQL-запрос ввиде строки или Executable объекта.
        :return: Результат запроса.
        """
        # Если запрос является строкой
        if isinstance(query, str):
            # То создаёт текстовый запрос из строки
            query = text(query)
        # Возвращает результат запроса
        return self._session.execute(query)
