   Проект реализует тестовый REST API сервис на Python, подробнее https://yadi.sk/i/dA9umaGbQdMNLw.   
  
   Установка на 'чистый' сервер Linux:  
  
1) Установка Python3.7   
	sudo apt install python3.7     
2) Установка среды виртуального окружения  
	sudo apt install python3-venv  
3) Установка менеджера пакетов  
	sudo apt install python3-pip   
4) Установка git  
	sudo apt install git  
5) Установка СУБД PostgreSQL  
  5.1 Установка СУБД  
     sudo apt install postgresql postgresql-contrib  
  5.2 Дополнительный пакет интеграции  
     sudo apt-get install postgresql-contrib libpq-dev python-dev  
  5.3 Скрипты для выполнения в psql:  
     5.3.1 Создание БД  
	CREATE DATABASE shop;   
     5.3.2 Создание пользователя для работы с сервисом и присвоение ему прав  
	CREATE USER shop_r WITH PASSWORD 'shop_r';  
	GRANT ALL PRIVILEGES ON DATABASE shop TO shop_r;  
6) Развертывание проекта, в данном случае с github:  
	git pull  
7) Создание виртуальной среды окружения:  
	python3 -m venv env    
	source env/bin/activate    
8) Установка python-пакетов для проекта:  
	pip3 install -r requirements.txt  
9) Создание структуры БД в среде python:  
	from rest_api import init_bd  
	init_bd()  
10) Запуск тестов:  
	python test.py  
11) Запуск сервиса:	  
	python run.py    

