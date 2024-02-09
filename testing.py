def explain_document_ml(spark_session):

    text = """ Patient with hypertension, syncope, and spinal stenosis - for recheck.
     (Medical Transcription Sample Report)
     SUBJECTIVE:
     The patient is a 78-year-old female who returns for recheck. She has hypertension. She denies difficulty with chest pain, palpations, orthopnea, nocturnal dyspnea, or edema.
     PAST MEDICAL HISTORY / SURGERY / HOSPITALIZATIONS:
     Reviewed and unchanged from the dictation on 12/03/2003.
     MEDICATIONS:
     Atenolol 50 mg daily, Premarin 0.625 mg daily, calcium with vitamin D two to three pills daily, multivitamin daily, aspirin as needed, and TriViFlor 25 mg two pills daily. She also has Elocon cream 0.1% and Synalar cream 0.01% that she uses as needed for rash."""

    data = spark_session.createDataFrame([[text]]).toDF("text")
    data.show(truncate = 60)


