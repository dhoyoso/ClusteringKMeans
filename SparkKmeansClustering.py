import sys
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import split
from pyspark.ml.feature import HashingTF, IDF, Tokenizer, CountVectorizer, StopWordsRemover
from pyspark.ml.clustering import KMeans
from pyspark.ml import Pipeline
from time import time
from pyspark.sql.functions import *

#Los argumentos son k, path de entrada, path de salida y lenguaje.

def main(argv):
	t1 = time()
	
	#se instancia el contexto de spark.	
	sc = SparkContext(appName="KMeans-Clustering-dhoyoso-dsernae")
	#se inicia sesion en spark.
	spark = SparkSession(sc)
	#se guarda el lenguaje a partir del cual se quitaran las stop words.
	language = argv[4]  #"spanish"
	#se guarda la ruta para la salida de los clusters.
	pathout = argv[3]
	#se guarda la ruta de la cual se leeran los archivos.
	path = argv[2] #"hdfs:///user/dhoyoso/datasets/dataset/"
	#se guarda el numero de clusters que se desea hacer.
	k = int(argv[1])  #4
	#se sacan los archivos a procesar a partir de la ruta.
	files = sc.wholeTextFiles(path)
	#se crea la estructura del dataframe; 2 columnas una para la ruta y otra para el texto.
	schema =  StructType([StructField ("path" , StringType(), True),StructField("text" , StringType(), True)])
	#se crea el dataframe a partir de la estructura y los archivos.
	df = spark.createDataFrame(files,schema)
	#se tokeniza el texto usando la clase de Ml tokenizer.
	tokenizer = Tokenizer(inputCol="text", outputCol="tokens")
	#se le dice al stop words remover que idioma es el que estamos tratando.
	StopWordsRemover.loadDefaultStopWords(language);
	#se remueven las stopwords de los tokens.
	stopWords = StopWordsRemover(inputCol="tokens", outputCol="stopWordsRemovedTokens")
	#se hace el hashing tf de los tokens restantes.	
	hashingTF = HashingTF(inputCol="stopWordsRemovedTokens", outputCol="rawFeatures", numFeatures=2000)
	#se hace el idf de la salida del hashingTF
	idf = IDF(inputCol="rawFeatures", outputCol="features", minDocFreq=1)
	#se inicializa el kmeans con el idf y el k deseado.
	kmeans = KMeans(k=k)
	#creacion del mapa de transformaciones.
	pipeline = Pipeline(stages=[tokenizer, stopWords, hashingTF, idf, kmeans])
	#inserta el dataframe como el inicio de las transformaciones
	model = pipeline.fit(df)
	#ejecuta las trasformaciones mapeadas y guarda el resultado
	results = model.transform(df)
	results.cache()
	#se corta la ruta para dejar solo el nombre y su respectivo cluster(prediction).
	split_col = split(results['path'], '/')
	results = results.withColumn('docname', split_col.getItem(7))
	df = results.select("docname", "prediction")

	t2 = time()
	
	print('Time:', t2-t1)	
	
	#se agrupan los documentos del mismo cluster en cluster_docs_list y se guardan en el path de salida como un json.
	grouped = df.groupBy(['prediction']).agg(collect_list("docname").alias('cluster_docs_list'))
	grouped.coalesce(1).write.json(path=pathout , mode = "overwrite")


if __name__ == "__main__":
	main(sys.argv)
