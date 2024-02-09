Follow the instructions here to install on Windows: 
    https://nlp.johnsnowlabs.com/docs/en/licensed_install#windows-support

PYTHON: 
    Install Python 3.8 to C:\Python38 and add C:\Python38\Scripts\ and C:\Python38\ to path in Windows environment variables

Download the license key file spark_nlp_for_healthcare_spark_ocr_****.json from https://my.johnsnowlabs.com/subscriptions 

Rename the file as spark_jsl.json and add it to the root of the project.

pip install -r requirements.txt

pip install spark-nlp-jsl==5.2.1  --extra-index-url https://pypi.johnsnowlabs.com/SECRET 
    
Here SECRET is 5.2.1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx from the spark_jsl.json file