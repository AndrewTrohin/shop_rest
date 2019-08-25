"""
    Модуль содержит запросы, необходимые для проверок, помежуточных действий
"""
def birthday_stat_sql(load_id):
    return f"select p.citizen_id, extract(MONTH from pr.birth_date) mes, count(*) presents \
             from person p,  unnest(relatives) as citizen(citizen_id) \
             inner join person pr on pr.citizen_id = citizen.citizen_id \
             where p.load_id = {load_id} and pr.load_id = p.load_id \
             group by p.citizen_id, mes"


def age_by_town_stat_sql(load_id):
    return f"select town, array_agg(extract(year from age(now(), birth_date))) \
             from person \
             where load_id = {load_id} \
             group by town"
