#import findspark
#findspark.init()

## main.py
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"

@app.route('/frame')
def frame():
    return render_template('index.html')



from pyspark.sql import SparkSession


import json
import psycopg2
import re
import csv
import pandas as pd
from collections import OrderedDict

from graphframes import *
import os

from sqlalchemy import create_engine




spark = SparkSession.builder \
       .master("local") \
       .appName("Spark") \
       .config("spark.some.config.option" , "some-value") \
       .config("spark.sql.repl.eagerEval.enabled", True) \
       .getOrCreate()


engine = create_engine('postgresql://parkhs:1234@postgres1:5432/postgres')
df = pd.read_sql_table('law_vertex', engine)
dfedge = pd.read_sql_table('law_edge', engine)

vv = spark.createDataFrame(df)
ee = spark.createDataFrame(dfedge)

g = GraphFrame(vv, ee)
g.cache()

@app.route('/insert_data')
def insert_data():
#    spark = SparkSession.builder \
#       .master("local") \
#       .appName("Spark") \
#       .config("spark.some.config.option" , "some-value") \
#       .config("spark.sql.repl.eagerEval.enabled", True) \
#       .getOrCreate()

    #conn = psycopg2.connect("dbname=postgres host=postgres1 user=parkhs password=1234")
    #cur = conn.cursor()
    
    path = "/www/src/webapp/"
    law_master_data = (
        spark.read.csv(
            path+'sample_data_vertex.csv',
            sep=",",
            header=True,
            quote='"',
            schema="id STRING", encoding='UTF-8'
        )
    )

    df = law_master_data.toPandas()

    law_edge_data = (
        spark.read.csv(
            path+'sample_data_edge.csv',
            sep=",",
            header=True,
            quote='"',
            schema="src STRING, dst STRING, support STRING", encoding='UTF-8'
        )
    )

    dfedge = law_edge_data.toPandas()

    #cur.execute("DROP TABLE IF EXISTS LAW_VERTEX")
    #cur.execute("DROP TABLE IF EXISTS LAW_EDGE")

    #conn.commit()


    engine = create_engine('postgresql://parkhs:1234@postgres1:5432/postgres')
    df.to_sql('law_vertex', con = engine, if_exists='replace', index=False)
    dfedge.to_sql('law_edge', con = engine, if_exists='replace', index=False)


    #conn.commit()
    #cur.close()
    #conn.close()
#    spark.stop()                    
    
    return "Success to insert data"



from pyvis.network import Network
import networkx as nx

import pyspark.sql.functions as F

@app.route('/test_search')
def test_search():
#    spark = SparkSession.builder \
#       .master("local") \
#       .appName("Spark") \
#       .config("spark.some.config.option" , "some-value") \
#       .config("spark.sql.repl.eagerEval.enabled", True) \
#       .getOrCreate()



#    engine = create_engine('postgresql://parkhs:1234@postgres1:5432/postgres')
#    df = pd.read_sql_table('law_vertex', engine)
#    dfedge = pd.read_sql_table('law_edge', engine)
    

    #spark.stop()



    return render_template('search.html', search_keyword = list(df['id']), start = 1, node_number = list(range(10)))


@app.route('/test_graph_search', methods=['POST', 'GET'])
def test_graph_search():

    law_name = request.args.get('graph_keyword1')
    law_name2 = request.args.get('graph_keyword2')
    node_number = int(request.args.get('node_number'))
    node_number2 = int(request.args.get('node_number2'))

#    spark = SparkSession.builder \
#       .master("local") \
#       .appName("Spark") \
#       .config("spark.some.config.option" , "some-value") \
#       .config("spark.sql.repl.eagerEval.enabled", True) \
#       .getOrCreate()



#    engine = create_engine('postgresql://parkhs:1234@postgres1:5432/postgres')
#    df = pd.read_sql_table('law_vertex', engine)
#    dfedge = pd.read_sql_table('law_edge', engine)

#    vv = spark.createDataFrame(df)
#    ee = spark.createDataFrame(dfedge)
    
#    g = GraphFrame(vv, ee)
#    g.cache()
    #law_name = "개인정보 보호법"
    #law_name2 = "민법"


    dataf = g.edges.where("src ='"+law_name +"'").orderBy(F.desc('support'))

    m_a = [row['src'] for row in dataf.collect()]
    m_b = [row['dst'] for row in dataf.collect()]
    m_c = [row['support'] for row in dataf.collect()]

    dataf1 = g.edges.where("src ='"+law_name2 +"'").orderBy(F.desc('support'))

    m_a1 = [row['src'] for row in dataf1.collect()]
    m_b1 = [row['dst'] for row in dataf1.collect()]
    m_c1 = [row['support'] for row in dataf1.collect()]

    nx_graph = nx.Graph()

    for i in range(0,node_number,1):
      nx_graph.add_node(i, size = 25 - 2*i, title=m_c[i], group =2, label=m_b[i])
      nx_graph.add_edge(i, 25, weight=m_c[i])
      if m_a1[0] == m_b[i]:
        for j in range (0,node_number2,1):
          nx_graph.add_node(j+50, size = 25 - 2*j, title=m_c1[j], group =4, label=m_b1[j])
          nx_graph.add_edge(j+50, i, weight=m_c1[j])  

    nx_graph.add_node(25, size=25, label=m_a[0], title='검색키', group=3)

    nt = Network('700px', '900px')

    nt.from_nx(nx_graph)


    #if os.path.exists('/www/src/webapp/templates/nx1.html'):
      #os.remove('/www/src/webapp/templates/nx1.html')


    nt.write_html('./webapp/templates/' + law_name + '_' + law_name2 + '.html')
#    spark.stop()
    #return print(dataf.show(1))
    return render_template(law_name + '_' + law_name2 + '.html')


@app.route('/test_get')
def test_get():
#    spark = SparkSession.builder \
#       .master("local") \
#       .appName("Spark") \
#       .config("spark.some.config.option" , "some-value") \
#       .config("spark.sql.repl.eagerEval.enabled", True) \
#       .getOrCreate()

  

    engine1 = create_engine('postgresql://parkhs:1234@postgres1:5432/postgres')
    df1 = pd.read_sql_table('law_vertex', engine1)
    dfedge1 = pd.read_sql_table('law_edge', engine1)
  
    vv = spark.createDataFrame(df1)
    ee = spark.createDataFrame(dfedge1)
    g = GraphFrame(vv, ee)
    g.cache()
#    spark.stop()
    return "Get Succesful"


@app.route('/test_graph')
def test_graph():
    nx_graph = nx.Graph()
    nx_graph.add_node(20, size=20, title='시행령', group=2, label='포항지진의 진상조사 및 피해구제 등을 위한 특별법')
    nx_graph.add_node(21, size=15, title='시행령', group=2, label='국방과학기술혁신 촉진법')
    nx_graph.add_node(22, size=25, title='법률', group=2, label='주민등록법')
    nx_graph.add_edge(20, 25, weight=5)
    nx_graph.add_edge(21, 25, weight=5)
    nx_graph.add_edge(22, 25, weight=5)
    nx_graph.add_node(25, size=25, label='평가 기준 1', title='개인정보 수집', group=3)
    
    nt = Network('700px', '700px')
    nt.from_nx(nx_graph)
    #nt.enable_physics(True)

    #if os.path.exists('./webapp/templates/nx.html'):
    #  os.removes('./webapp/templates/nx.html')
    
    nt.write_html('./webapp/templates/nx.html')

    return render_template('nx.html')

 
