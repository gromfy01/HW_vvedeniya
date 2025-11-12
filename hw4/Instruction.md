# Инструкция по развёртыванию кластера Hive

Инструкция hw3 выполняются при условии, что выполнены шаги инструкций hw1 и hw2


1. **Все действия выполняем на jn ноде**
```bash
ssh team@176.109.91.44
```

2. **Склонировать github репозиторий**
```bash
git clone https://github.com/gromfy01/HW_vvedeniya.git
```

3. **Перейти в директорию hw4/**
```bash
cd HW_vvedeniya/hw4
```

4. **Перейти в поддиректорию ansible/**
```bash
cd ansible
```

5. **Запустить Ansible playbook и на запрос ввести пароль пользователя team**
```bash
ansible-playbook -i inventory.ini install_configure_hive.yml --ask-become-pass
```

Он разворачивает hive, выполняет проверки корректности установки, загружает датасет и создаёт таблицы. 

6. **Запустить ssh туннели и проверить доступность web-интерфейсов**

```bash
ssh -L 10002:192.168.1.35:10002 -L 9870:192.168.1.35:9870 -L 8042:192.168.1.35:8042 -L 19888:192.168.1.35:19888 -L 8088:192.168.1.35:8088 team@176.109.91.44
```
После этого в браузере откройте: [http://localhost:10002/](http://localhost:10002/)

7. **Вызовем beeline**
```bash
beeline -u jdbc:hive2://nn:5433
```

8. Создадим базу данных
```sql
CREATE DATABASE test;
```

9. Проверим HIVE http://localhost:10002
В Lаst Max 25 Closed Queries можем увидеть результат.

10. Проверим HDFS http://localhost:9870/explorer.html#/user/hive/warehouse
В /user/hive/warehouse  видим test.db.

11. Загрузить тестовый датасет
```bash
# Создать папку input в HDFS (если её ещё нет)
hdfs dfs -mkdir -p /user/hadoop/input

# Проверить, что она создалась
hdfs dfs -ls /user/hadoop

# Загрузить локальный файл data.parquet в HDFS
hdfs dfs -put /tmp/data.parquet /user/hadoop/input/

# Проверить, что файл на месте
hdfs dfs -ls /user/hadoop/input
```

12. Копирование python скрипта для трансформаций.
```
sudo cp /home/team/HW_vvedeniya/hw4/transform.py /home/hadoop/
```

13. Запустить python скрипт, который применяет следующие трансформации:
 - **Чтение** Parquet-файла из HDFS в DataFrame.
- **Очистка данных** — замена пропусков (`NULL`) на нули в числовых колонках.
- **Добавление метрик** — вычисляются новые столбцы:
    - `kda` = (kills + assists) / deaths (или kills + assists, если deaths = 0);
    - `efficiency` = gold_per_min + xp_per_min.
- **Агрегация** — группировка по `hero_id` и расчёт средних значений (kills, deaths, assists, kda, efficiency) и числа матчей (`matches_played`).
- **Фильтрация** — оставляются только герои с 500 и более матчами.
- **Партиционирование** — объединение данных в одну партицию.
- **Сохранение результата** — запись итоговых данных в HDFS (Parquet) и в таблицу Hive `test.dota_heroes_stats`.
```bash
source venv/bin/activate
python3 transform.py
```

14. Смотрим содержимое test.db: http://localhost:9870/explorer.html#/user/hive/warehouse/test.db/

Структура репозитория

```bash
hw4/
├── Instruction.md
├── transform.py
└── ansible/
    ├── inventory.ini    
    ├── roles/
    │   │
    │   └── spark
    │       └── tasks/
    │           └── main.yml       
    ├── files/
    └── setup_jn.yml
```
