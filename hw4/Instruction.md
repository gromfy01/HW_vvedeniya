# Инструкция по развёртыванию кластера Hive

Инструкция hw4 выполняются при условии, что выполнены шаги инструкций hw1, hw2, hw3


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
ansible-playbook -i inventory.ini setup_jn.yml --ask-become-pass
```

Он разворачивает spark. 

6. **Запустить ssh туннели и проверить доступность web-интерфейсов**

```bash
ssh -L 10002:192.168.1.35:10002 -L 9870:192.168.1.35:9870 -L 8042:192.168.1.35:8042 -L 19888:192.168.1.35:19888 -L 8088:192.168.1.35:8088 team@176.109.91.44
```
После этого в браузере откройте: [http://localhost:10002/](http://localhost:10002/)

7. **Вызовем beeline**
```bash
# перейти под пользователя root
sudo su -
# ввести пароль
# перейти под пользователя hadoop
su - hadoop
beeline -u jdbc:hive2://nn:5433
```

8. **Создадим базу данных**
```sql
CREATE DATABASE test;
!q
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
hdfs dfs -put /tmp/people-10000.parquet /user/hadoop/input/

# Проверить, что файл на месте
hdfs dfs -ls /user/hadoop/input
```

12. Зaпускаем ipython.
```bash
source venv/bin/activate
ipython
```

13. Выполняем импорты необходимых библиотек.
```python
from onetl.connection import Hive, SparkHDFS
from pyspark.sql import SparkSession
from pyspark.sql.functions import concat, col, lit, length, split, when, count, avg, min, max, desc
from onetl.db import DBWriter
from onetl.file import FileDFReader
from onetl.file.format import Parquet
```

14. Создаём Spark сессию.
```python
spark = (
    SparkSession.builder.master("yarn")
    .appName('test.people_transformations')
    .config("spark.sql.warehouse.dir", "/user/hive/warehouse")
    .config("spark.hive.metastore.uris", "thrift://nn:9083")
    .enableHiveSupport()
    .getOrCreate()
)
```

15. Инициализация HDFS кластера
```python
hdfs = SparkHDFS(host="nn", port=9000, spark=spark, cluster="x")
hdfs.check()
```

16. Читаем датасет
```python
reader = FileDFReader(connection=hdfs, format=Parquet(), source_path="/user/hadoop/input")
df = reader.run(["people-10000.parquet"])
df.count()
```

17. Инициализация Hive
```python
hive = Hive(spark=spark, cluster="x")
hive.check()
```

18. Выполнение трансформаций. Очистка данных - замена NULL значений.
```python
df_cleaned = df.fillna({
    'First Name': 'Unknown',
    'Last Name': 'Unknown',
    'Sex': 'Unknown',
    'Email': 'unknown@example.com',
    'Phone': 'Unknown',
    'Job Title': 'Unknown'
})
```

19. Добавление вычисляемых полей на основе существующих данных
```python
df_with_metrics = df_cleaned \
    .withColumn("full_name", concat(col("First Name"), lit(" "), col("Last Name"))) \
    .withColumn("name_length", length(col("full_name"))) \
    .withColumn("email_domain", split(col("Email"), "@").getItem(1)) \
    .withColumn("name_complexity", 
               when(col("name_length") < 10, "Simple")
               .when((col("name_length") >= 10) & (col("name_length") < 15), "Medium")
               .otherwise("Complex"))
```

20. Агрегация данных по различным критериям
```python
# Аналитическая агрегация по сложности имен
name_complexity_stats = df_with_metrics.groupBy("name_complexity").agg(
    count("*").alias("count_people"),
    avg("name_length").alias("avg_name_length"),
    min("name_length").alias("min_name_length"),
    max("name_length").alias("max_name_length")
)
name_complexity_stats.show()

# Аналитическая агрегация по доменам email
email_stats = df_with_metrics.groupBy("email_domain").agg(
    count("*").alias("user_count")
).orderBy(desc("user_count")).limit(10)
email_stats.show()

# Аналитическая агрегация по полу
gender_stats = df_with_metrics.groupBy("Sex").agg(
    count("*").alias("count"),
    avg("name_length").alias("avg_name_length")
)
gender_stats.show()
```

21. Сохранение в Hive основной датафрейм с партиционированием.
```python
writer = DBWriter(connection=hive, target="test.people_with_metrics", options={"partitionBy": "name_complexity"})
writer.run(df_with_metrics)
```

22. Останавливаем Spark сессию.
```python
spark.stop()
```

23. Смотрим содержимое test.db: http://localhost:9870/explorer.html#/user/hive/warehouse/test.db/people_with_metrics

---

Структура репозитория

```
hw4/
├── Instruction.md
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
