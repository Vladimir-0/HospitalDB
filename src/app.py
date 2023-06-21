from typing import Tuple, Optional

from sqlalchemy import select, join, func
from tabulate import tabulate

from . import HospitalDB


class HospitalApp:
    def __init__(self, hospital_db: HospitalDB) -> None:
        """
        Программа для работы с базой данных HospitalDB.
        :param hospital_db: Экземпляр класса HospitalDB.
        """
        self.hospital_db = hospital_db
        self._run = False

    def run(self) -> None:
        """
        Запускает программу в консоли
        """
        self._run = True
        while self._run:
            command: str | None
            args: list[str] | None
            command, args = self._get_input()
            if command is None:
                continue
            try:
                self._execute_command(command, args)
            except Exception as e:
                print("Error:", e)

    @staticmethod
    def _get_input() -> Tuple[Optional[str], Optional[list[str]]]:
        """
        Принимает ввод из консоли и отделяет команду от аргументов.
        :return: Список из команды и её аргументов.
        """
        inp: list[str] = input("> ").split()
        if inp:
            command: str = inp.pop(0)
            args: list[str] = inp
        else:
            command: Optional[str] = None
            args: Optional[list[str]] = None
        return command, args

    def _execute_command(self, command: str, args: list[str]) -> None:
        """
        Выполняет введённую пользователем команду.
        :param command: Команда.
        :param args: Аргументы команды.
        """
        if command == "exit":
            self._run = False
        elif command == "get_all_orders":
            self.get_all_orders()
        elif command == "get_by_order_id":
            self.get_by_order_id(int(args[0]))
        elif command == "earning_by_group":
            self.group_by_groups()
        elif command == "earning_by_month":
            self.group_by_months()
        elif command == "help":
            self.help()
        else:
            self.unknown_command()

    def get_all_orders(self) -> None:
        """
        Выводит в консоль таблицу со всеми заказами.
        """
        headers = ["id", "Дата", "Время", "Группа анализов", "Название анализа", "Цена"]

        o = self.hospital_db.Orders
        g = self.hospital_db.Groups
        a = self.hospital_db.Analyses

        data = self.hospital_db.execute(
            select(o.id, o.date + o.time, g.name, a.name, a.price)
            .select_from(
                join(o, a, o.analise_id == a.id)
                .join(g, a.group_id == g.id)
            )
        )
        print(tabulate(data.fetchall(), headers))

    def group_by_groups(self) -> None:
        """
        Выводит в консоль общую прибыль для каждой группы анализов.
        """
        headers = ["Группа анализов", "Общая прибыль"]

        o = self.hospital_db.Orders
        g = self.hospital_db.Groups
        a = self.hospital_db.Analyses

        data = self.hospital_db.execute(
            select(g.name, func.sum(a.price))
            .select_from(
                join(o, a, o.analise_id == a.id)
                .join(g, a.group_id == g.id)
            ).group_by(g.name)
        )
        print(tabulate(data.fetchall(), headers))

    def get_by_order_id(self, order_id: int) -> None:
        """
        Выводит в консоль заказ с указанным id.
        :param order_id: id заказа.
        """
        headers = ["id", "Дата", "Время", "Группа анализов", "Название анализа", "Цена"]
        if not isinstance(order_id, int):
            return

        o = self.hospital_db.Orders
        g = self.hospital_db.Groups
        a = self.hospital_db.Analyses

        data = self.hospital_db.execute(
            select(o.id, o.date + o.time, g.name, a.name, a.price)
            .select_from(
                join(o, a, o.analise_id == a.id)
                .join(g, a.group_id == g.id)
            ).where(o.id == order_id)
        )
        print(tabulate(data.fetchall(), headers))

    def group_by_months(self) -> None:
        """
        Выводит в консоль общую прибыль за каждый месяц.
        """
        headers = ["Месяц", "Общая прибыль"]

        o = self.hospital_db.Orders
        g = self.hospital_db.Groups
        a = self.hospital_db.Analyses

        data = self.hospital_db.execute(
            select(func.date_trunc('month', o.date).label('month'), func.sum(a.price))
            .select_from(
                join(o, a, o.analise_id == a.id)
                .join(g, a.group_id == g.id)
            ).group_by('month')
        )
        print(tabulate(data.fetchall(), headers))

    @staticmethod
    def unknown_command() -> None:
        """
        Выводит в консоль сообщение о неизвестной команде.
        """
        print("Неизвестная команда")

    @staticmethod
    def help() -> None:
        """
        Выводит в консоль таблицу со всеми командами и их описанием.
        """
        headers: tuple[str, str] = ("Команда", "Описание")
        _help: tuple[tuple[str, str], ...] = (
            (
                "get_all_orders",
                "Выводит все заказы на экран"
            ),
            (
                "get_by_order_id <order_id>",
                "Выводит заказ с указанным id"
            ),
            (
                "earning_by_group",
                "Выводит данные о доходах, полученных из всех типов анализов"
            ),
            (
                "earning_by_month",
                "Выводит данные о доходах, по месяцам"
            ),
            (
                "exit",
                "Выход из программы"
            )
        )
        print(tabulate(tabular_data=_help, headers=headers))
