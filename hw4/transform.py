from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, avg, count, round as rnd

# Создаём SparkSession с поддержкой Hive
spark = (
    SparkSession.builder
    .appName("dota_parquet_transformations")
    .master("yarn")
    .config("spark.sql.warehouse.dir", "/user/hive/warehouse")
    .config("spark.hive.metastore.uris", "thrift://nn:9083")
    .enableHiveSupport()
    .getOrCreate()
)

# Пути к данным (в HDFS)
input_path = "hdfs:///user/hadoop/input/data.parquet"
output_path = "hdfs:///user/hadoop/output/dota_transformed"

# Чтение Parquet-данных из HDFS
df = spark.read.parquet(input_path)

print("Количество строк:", df.count())
df.printSchema()


# Трансформации данных

# Заполняем пропуски нулями в числовых колонках
num_cols = ["kills", "deaths", "assists", "gold", "last_hits", "denies",
            "gold_per_min", "xp_per_min", "hero_damage", "tower_damage"]

df_clean = df.fillna(0, subset=num_cols)


# Создание производных метрик

# Добавляем новую колонку KDA (отношение убийств + ассистов к смертям)
df_kda = df_clean.withColumn(
    "kda",
    when(col("deaths") == 0, col("kills") + col("assists"))
    .otherwise((col("kills") + col("assists")) / col("deaths"))
)

# Добавляем колонку эффективности фарма (gold_per_min + xp_per_min)
df_kda = df_kda.withColumn(
    "efficiency",
    col("gold_per_min") + col("xp_per_min")
)

# Группировка и агрегация
df_agg = (
    df_kda.groupBy("hero_id")
    .agg(
        rnd(avg("kills"), 2).alias("avg_kills"),
        rnd(avg("deaths"), 2).alias("avg_deaths"),
        rnd(avg("assists"), 2).alias("avg_assists"),
        rnd(avg("kda"), 2).alias("avg_kda"),
        rnd(avg("efficiency"), 2).alias("avg_efficiency"),
        count("*").alias("matches_played")
    )
)

# Добавление фильтра
df_filtered = df_agg.filter(col("matches_played") >= 500)


# Партиционирование и сохранение результата

# repartition для контроля количества файлов (например, по 1 на партицию)
df_partitioned = df_filtered.repartition(1)

# Запись в HDFS в формате Parquet
df_partitioned.write.mode("overwrite").parquet(output_path)

# Сохранение в Hive как таблицы
df_partitioned.write.mode("overwrite").saveAsTable("test.dota_heroes_stats")

# Завершение сессии
spark.stop()
