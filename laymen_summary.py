from pyspark.ml import Pipeline
from sparknlp import DocumentAssembler
from sparknlp.pretrained import PretrainedPipeline
from sparknlp_jsl.annotator import MedicalSummarizer
from print_summary import print_summary


def summarizer_clinical_laymen_onnx_pipeline(input_text):
    pipeline = PretrainedPipeline("summarizer_clinical_laymen_onnx_pipeline", "en", "clinical/models")

    result = pipeline.fullAnnotate(input_text)
    print_summary(result, 'NLP 5.2.0+ CLINICAL LAYMEN ONNX PIPELINE')


def summarizer_clinical_laymen_onnx(spark, input_text):
    document_assembler = DocumentAssembler() \
        .setInputCol("text") \
        .setOutputCol("document")
    summarizer = MedicalSummarizer.pretrained("summarizer_clinical_laymen_onnx", "en", "clinical/models") \
        .setInputCols(["document"]) \
        .setOutputCol("summary") \
        .setMaxNewTokens(512)
    pipeline = Pipeline(stages=[
        document_assembler,
        summarizer
    ])

    data = spark.createDataFrame([[input_text]]).toDF("text")
    result = pipeline.fit(data).transform(data)
    print_summary(result.collect(), 'NLP 5.0.1+ CLINICAL LAYMEN ONNX')


def summarizer_clinical_laymen_pipeline(input_text):
    pipeline = PretrainedPipeline("summarizer_clinical_laymen_pipeline", "en", "clinical/models")

    result = pipeline.fullAnnotate(input_text)
    print_summary(result, 'NLP 4.4.1+, NLP 4.4.4+ CLINICAL LAYMEN PIPELINE')


def summarizer_clinical_laymen(spark, input_text):
    document_assembler = DocumentAssembler() \
        .setInputCol("text") \
        .setOutputCol("document")

    summarizer = MedicalSummarizer.pretrained("summarizer_clinical_laymen", "en", "clinical/models") \
        .setInputCols(["document"]) \
        .setOutputCol("summary") \
        .setMaxNewTokens(512)

    pipeline = Pipeline(stages=[
        document_assembler,
        summarizer
    ])

    data = spark.createDataFrame([[input_text]]).toDF("text")
    result = pipeline.fit(data).transform(data)
    print_summary(result.collect(), 'NLP 4.4.2+ CLINICAL LAYMEN')