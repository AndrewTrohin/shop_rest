# shop_rest

В проекте используется PostgresSQL.  
Создание базы данных  - CREATE DATABASE shop;  
Создание пользователя postgres -  CREATE USER postgres WITH PASSWORD 'postgres';  
Создание прав пользователю - GRANT ALL PRIVILEGES ON DATABASE shop TO postgres;  
  
Для установки необходимых пакетов нужно выполнить:  
	pip3 install -r requirements.txt    
  
Для создания таблиц нужно в папке проекта выполнить питоновский код:  
	from rest_api import init_bd  
	init_bd()  

  


Для запуска проета запустить файл run.py  


Запуск тестов  python test.py  
