from prefect import flow, task
from onetl.connection import Hive, SparkHDFS
from pyspark.sql import SparkSession
from pyspark.sql.functions import concat, col, lit, length, split, when, count, avg, min, max, desc
from onetl.db import DBWriter
from onetl.file import FileDFReader
from onetl.file.format import Parquet


@task
def init_spark():
    """Задача для инициализации Spark сессии"""
    spark = (
        SparkSession.builder.master("yarn")
        .appName('test.people_transformations')
        .config("spark.sql.warehouse.dir", "/user/hive/warehouse")
        .config("spark.hive.metastore.uris", "thrift://nn:9083")
        .enableHiveSupport()
        .getOrCreate()
    )
    return spark


@task
def stop_spark(spark):
    """Задача для остановки Spark сессии"""
    spark.stop()


@task
def extract(spark):
    """Задача для чтения данных из HDFS"""
    hdfs = SparkHDFS(host="nn", port=9000, spark=spark, cluster="x")
    hdfs.check()
    
    reader = FileDFReader(connection=hdfs, format=Parquet(), source_path="/user/hadoop/input")
    df = reader.run(["people-10000.parquet"])
    
    print(f"Данные загружены: {df.count()} записей")
    return df


@task
def transform(df):
    """Задача для трансформации данных"""
    # Очистка данных - замена NULL значений
    df_cleaned = df.fillna({
        'First Name': 'Unknown',
        'Last Name': 'Unknown',
        'Sex': 'Unknown',
        'Email': 'unknown@example.com',
        'Phone': 'Unknown',
        'Job Title': 'Unknown'
    })
    
    # Добавление вычисляемых полей
    df_with_metrics = df_cleaned \
        .withColumn("full_name", concat(col("First Name"), lit(" "), col("Last Name"))) \
        .withColumn("name_length", length(col("full_name"))) \
        .withColumn("email_domain", split(col("Email"), "@").getItem(1)) \
        .withColumn("name_complexity", 
                   when(col("name_length") < 10, "Simple")
                   .when((col("name_length") >= 10) & (col("name_length") < 15), "Medium")
                   .otherwise("Complex"))
    
    print("Трансформации применены успешно")
    return df_with_metrics


@task
def analyze_data(df_with_metrics):
    """Задача для аналитической агрегации данных"""
    # Аналитическая агрегация по сложности имен
    name_complexity_stats = df_with_metrics.groupBy("name_complexity").agg(
        count("*").alias("count_people"),
        avg("name_length").alias("avg_name_length"),
        min("name_length").alias("min_name_length"),
        max("name_length").alias("max_name_length")
    )
    print("Аналитическая агрегация по сложности имен:")
    name_complexity_stats.show()
    
    # Аналитическая агрегация по доменам email
    email_stats = df_with_metrics.groupBy("email_domain").agg(
        count("*").alias("user_count")
    ).orderBy(desc("user_count")).limit(10)
    print("Аналитическая агрегация по доменам email:")
    email_stats.show()
    
    # Аналитическая агрегация по полу
    gender_stats = df_with_metrics.groupBy("Sex").agg(
        count("*").alias("count"),
        avg("name_length").alias("avg_name_length")
    )
    print("Аналитическая агрегация по полу:")
    gender_stats.show()
    
    return df_with_metrics


@task
def load(spark, df_with_metrics):
    """Задача для сохранения данных в Hive"""
    hive = Hive(spark=spark, cluster="x")
    hive.check()
    
    writer = DBWriter(
        connection=hive, 
        target="test.people_with_metrics_prefect", 
        options={"partitionBy": "name_complexity"}
    )
    writer.run(df_with_metrics)
    
    print("Данные сохранены в Hive таблицу test.people_with_metrics_prefect")


@flow
def process_people_data():
    """Основной поток обработки данных"""
    spark = init_spark()
    
    try:
        df = extract(spark)
        df_with_metrics = transform(df)
        df_with_metrics = analyze_data(df_with_metrics)
        load(spark, df_with_metrics)
        print("Все шаги выполнены успешно!")
        
    except Exception as e:
        print(f"Ошибка в процессе обработки: {str(e)}")
        raise
    
    finally:
        stop_spark(spark)


if __name__ == "__main__":
    process_people_data()

