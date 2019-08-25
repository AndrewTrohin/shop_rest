from .models import db


def execute_sql(sql_text):
    """
    Выполняет sql-запрос sql_text и возвращает результат
    """
    result = db.engine.execute(sql_text)
    return result


def check_sql_has_result(sql_text):
    """
    Выполняет sql-запрос и возвращет True, если данные, иначе False
    """
    return True if execute_sql(sql_text).fetchall() else False