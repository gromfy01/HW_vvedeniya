# Инструкция по обработке данных с помощью prefect

Инструкция hw5 выполняются при условии, что выполнены шаги инструкций hw1, hw2, hw3, hw4.


1. **Все действия выполняем на jn ноде**
```bash
ssh team@176.109.91.44
```

2. **Склонировать github репозиторий**
```bash
git clone https://github.com/gromfy01/HW_vvedeniya.git
```

3. **Перейти в директорию hw5/**
```bash
cd HW_vvedeniya/hw5
```

6. **Запустить ssh туннели и проверить доступность web-интерфейсов**

```bash
ssh -L 10002:192.168.1.35:10002 -L 9870:192.168.1.35:9870 -L 8042:192.168.1.35:8042 -L 19888:192.168.1.35:19888 -L 8088:192.168.1.35:8088 team@176.109.91.44
```
После этого в браузере откройте: [http://localhost:10002/](http://localhost:10002/)

10. Проверим HDFS http://localhost:9870/explorer.html#/user/hive/warehouse
В /user/hive/warehouse  видим test.db.

11. Загрузить тестовый датасет
```bash
# Создать папку input в HDFS (если её ещё нет)
hdfs dfs -mkdir -p /user/hadoop/input

# Проверить, что она создалась
hdfs dfs -ls /user/hadoop

# Загрузить локальный файл data.parquet в HDFS
hdfs dfs -put /tmp/people-10000.parquet /user/hadoop/input/

# Проверить, что файл на месте
hdfs dfs -ls /user/hadoop/input
```

12. Зaпускаем скрипт.
```bash
source venv/bin/activate
python3 prefect.py
```

23. Смотрим содержимое test.db: http://localhost:9870/explorer.html#/user/hive/warehouse/test.db/people_with_metrics_prefect

---

Структура репозитория

```
hw5/
├── Instruction.md
└── prefect.py
```
