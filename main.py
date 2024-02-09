import json
import os

import sparknlp
import sparknlp_jsl
from sparknlp_jsl.annotator import *
import pandas as pd
import warnings
from sparknlp.pretrained import ResourceDownloader
import subprocess

from data import input1, input2, input3, input4
from laymen_summary import summarizer_clinical_laymen_onnx_pipeline, summarizer_clinical_laymen_onnx, \
    summarizer_clinical_laymen_pipeline, summarizer_clinical_laymen


def get_java_version():
    try:
        # Run the command to get the Java version
        result = subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT)
        lines = result.splitlines()
        for line in lines:
            line = line.decode('utf-8')
            if line.startswith('java version'):
                return line.split()[2].replace('"', '')
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode('utf-8'))

def start_spark_session():
    with open('spark_jsl.json') as f:
        license_keys = json.load(f)

    os.environ["SPARK_NLP_LICENSE"] = license_keys['SPARK_NLP_LICENSE']

    pd.set_option('display.max_colwidth', 200)
    warnings.filterwarnings('ignore')
    params = {"spark.driver.memory": "16G",
              "spark.kryoserializer.buffer.max": "2000M",
              "spark.driver.maxResultSize": "2000M"}

    return sparknlp_jsl.start(license_keys['SECRET'], params=params)

if __name__ == "__main__":
    # Start the Spark session
    spark_session = start_spark_session()

    # Show available pipelines
    ResourceDownloader.showPublicPipelines(lang="en")

    # Show installation versions
    java_version = get_java_version()
    print("Java version:", java_version)
    print("Apache Spark version:", spark_session.version)
    print("Spark NLP Version :", sparknlp.version())
    print("Spark NLP_JSL Version :", sparknlp_jsl.version())

    # Show summaries
    input('\nPRESS ENTER TO CONTINUE\n')
    summarizer_clinical_laymen_onnx_pipeline(input1)
    input('\nPRESS ENTER TO CONTINUE\n')
    summarizer_clinical_laymen_onnx(spark_session, input2)
    input('\nPRESS ENTER TO CONTINUE\n')
    summarizer_clinical_laymen_pipeline(input3)
    input('\nPRESS ENTER TO CONTINUE\n')
    summarizer_clinical_laymen(spark_session, input4)