# Big data text clustering using KMeans

An implementation of KMeans text clustering made in Python and Apache Spark.

## Getting Started

### Prerequisites

- [hortonworks Cluster](https://hortonworks.com/) ->  2.6.3
- Python -> 3.6
- Spark -> 2.1.1
- Scala -> 2.11.8
- Java JRE -> 1.8.0_144

### Setting up Spark
Assuming you already have installed JAVA and Python.

1. Visit the Spark downloads page.
2. Select the latest Spark release, a prebuilt package for Hadoop 2.4,and download directly.

Then you'll have to figure out how to go about things depending on your operating system.

on a POSIX OS:

1. Unzip Spark.
2. Move the unzipped directory to a working application directory.
3. Edit the bash profile to add Spark to your PATH and set SPARK_HOME environment variable. 
```
export SPARK_HOME=/home/ubuntu/spark/spark-1.4.1-bin-hadoop2.6
export PATH=$SPARK_HOME/bin:$PATH
```
Testing PySpark:
```
$ pyspark --version

SPARK_MAJOR_VERSION is set to 2, using Spark2
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 2.1.1.2.6.1.0-129
      /_/

Using Scala version 2.11.8, Java HotSpot(TM) 64-Bit Server VM, 1.8.0_144
Branch HEAD
Compiled by user jenkins on 2017-05-31T03:30:24Z
Revision e6dcaa0cd2f08f003ac34af03097c2f41209f065
Url git@github.com:hortonworks/spark2.git
Type --help for more information.

```

At this point Spark is installed and ready to use on your local machine in "standalone mode.", You can also set it up in a n-node [Spark cluster](https://amilasnotes.wordpress.com/2015/09/06/setting-up-a-two-node-spark-cluster/)

### Usage

The code receive three parameters to work this are:
1. The number of documents clusters you want to generate.
2. The HDFS path to the documents. (for example: hdfs:///user/dhoyoso/datasets/dataset/)
3. The language of the documents for stopwords removing.The input language should be at english for example: danish, dutch, english, finnish, french, german, hungarian, spanish, swedish, turkish, etc.)

1. For local usage:

Parameters: K = 4, PATH = hdfs:///user/dhoyoso/datasets/gutenberg-txt-es/, STOPWORDSLANGUAGE = spanish.

```
$spark-submit --master local --deploy-mode client SparkKmeansClustering.py 4 hdfs:///user/datasets/gutenberg-txt-es/ spanish 
```
Output: clusteringOut.txt

2. Using all the Hadoop Cluster:

Code Parameters: K = 4, PATH = hdfs:///user/dhoyoso/datasets/gutenberg-txt-es/, STOPWORDSLANGUAGE = spanish.
r
Clustering parameters: --master <resource negotiators like yarn or locals> --deploy-mode <How to deploy or execute, cluster or client>  --executor-memory <The amount of memory you would give at maximum to this process> --num-executors <number of executors>

```
$spark-submit --master yarn --deploy-mode cluster --executor-memory 2G --num-executors 4 SparkKmeansClustering.py 4 hdfs:///user/datasets/gutenberg-txt-es/ spanish 
```
Output: clusteringOut.txt

For further usage options and other issues please read the subtmitting applications [full documentation](https://spark.apache.org/docs/2.1.1/submitting-applications.html)

## Authors

* **Daniel Hoyos Ospina**
* **Daniela Serna Escobar**

## Acknowledgments

* Edwin Nelson Montoya Múnera
* Juan David Pineda Cardenas
* Edwin Montoya Jaramillo
* Diego Alejandro Perez Gutierrez
* Daniel Rendon 
* Laura Mejia
