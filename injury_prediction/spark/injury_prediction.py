from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.regression import LinearRegression
from pyspark.ml import Pipeline
from pyspark.sql.types import *
import json

def create_spark_session():
    return SparkSession.builder \
        .appName("InjuryPrediction") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0") \
        .getOrCreate()

def read_from_kafka(spark):
    return spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "fitness_features") \
        .load()

def process_stream(df):
    # Parse JSON data with updated schema
    schema = StructType([
        StructField("user_id", IntegerType()),
        StructField("activity_date", StringType()),
        StructField("cadence_speed_ratio", DoubleType()),
        StructField("strain_per_mile", DoubleType()),
        StructField("activity_intensity", DoubleType()),
        StructField("recovery_ratio", DoubleType()),
        StructField("age", IntegerType()),
        StructField("sex", StringType()),
        StructField("miles", DoubleType()),
        StructField("av_cadence", DoubleType()),
        StructField("av_speed", DoubleType()),
        StructField("exercise_strain", IntegerType()),
        StructField("sleep_hours", DoubleType())
    ])
    
    # Convert JSON string to structured data
    parsed_df = df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")
    
    # Feature engineering with additional metrics
    feature_cols = [
        "cadence_speed_ratio",
        "strain_per_mile",
        "activity_intensity",
        "recovery_ratio",
        "age",
        "miles",
        "av_cadence",
        "av_speed",
        "exercise_strain"
    ]
    
    # Convert sex to numeric
    sex_indexer = StringIndexer(inputCol="sex", outputCol="sex_index")
    
    # Assemble features
    assembler = VectorAssembler(
        inputCols=feature_cols + ["sex_index"],
        outputCol="features"
    )
    
    # Create pipeline
    pipeline = Pipeline(stages=[sex_indexer, assembler])
    model = pipeline.fit(parsed_df)
    transformed_df = model.transform(parsed_df)
    
    return transformed_df

def train_model(df):
    # Split data for training
    train_df, test_df = df.randomSplit([0.8, 0.2])
    
    # Train linear regression model with updated features
    lr = LinearRegression(
        featuresCol="features",
        labelCol="exercise_strain",  # Using exercise_strain as the target variable
        maxIter=10,
        regParam=0.3,
        elasticNetParam=0.8
    )
    
    # Fit model
    lr_model = lr.fit(train_df)
    
    # Make predictions
    predictions = lr_model.transform(test_df)
    
    return predictions, lr_model

def write_to_kafka(df):
    # Add prediction interpretation
    df_with_risk = df.withColumn(
        "injury_risk",
        when(col("prediction") > 7, "High")
        .when(col("prediction") > 5, "Medium")
        .otherwise("Low")
    )
    
    return df_with_risk.select(
        to_json(struct(
            "user_id",
            "activity_date",
            "prediction",
            "injury_risk",
            "cadence_speed_ratio",
            "strain_per_mile"
        )).alias("value")
    ).writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("topic", "injury_predictions") \
        .option("checkpointLocation", "/tmp/checkpoint") \
        .start()

def main():
    spark = create_spark_session()
    
    # Read from Kafka
    df = read_from_kafka(spark)
    
    # Process stream
    processed_df = process_stream(df)
    
    # Train model and get predictions
    predictions, model = train_model(processed_df)
    
    # Write predictions back to Kafka
    query = write_to_kafka(predictions)
    
    # Wait for the streaming to finish
    query.awaitTermination()

if __name__ == "__main__":
    main() 