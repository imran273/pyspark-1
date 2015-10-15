from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, Row, StringType

conf = SparkConf().setAppName("spark_sql_udf")

sc = SparkContext(conf=conf)

sqlCtx = SQLContext(sc)

lines = sc.parallelize(["a", "b", "c"])

people = lines.map(lambda value: Row(name=value))

peopleSchema = sqlCtx.createDataFrame(people)

peopleSchema.registerTempTable("people")


def myfunc(value):
    return value.upper()

sqlCtx.registerFunction("myfunc", myfunc, StringType())

rows = sqlCtx.sql("select myfunc(name) from people").collect()

sc.stop()

for row in rows:
    print row