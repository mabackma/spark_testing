input1 = """Olivia Smith was seen in my office for evaluation for elective surgical weight loss on October 6, 2008. Olivia Smith is a 34-year-old female with a BMI of 43. She is 5'6" tall and weighs 267 pounds. She is motivated to attempt surgical weight loss because she has been overweight for over 20 years and wants to have more energy and improve her self-image. She is not only affected physically, but also socially by her weight. When she loses weight she always regains it and she always gains back more weight than she has lost. At one time, she lost 100 pounds and gained the weight back within a year. She has tried numerous commercial weight loss programs including Weight Watcher's for four months in 1992 with 15-pound weight loss, RS for two months in 1990 with six-pound weight loss, Slim Fast for six weeks in 2004 with eight-pound weight loss, an exercise program for two months in 2007 with a five-pound weight loss, Atkin's Diet for three months in 2008 with a ten-pound weight loss, and Dexatrim for one month in 2005 with a five-pound weight loss. She has also tried numerous fat reduction or fad diets. She was on Redux for nine months with a 100-pound weight loss.

    PAST MEDICAL HISTORY: She has a history of hypertension and shortness of breath.

    PAST SURGICAL HISTORY: Pertinent for cholecystectomy.

    PSYCHOLOGICAL HISTORY: Negative.

    SOCIAL HISTORY: She is single. She drinks alcohol once a week. She does not smoke.

    FAMILY HISTORY: Pertinent for obesity and hypertension.

    MEDICATIONS: Include Topamax 100 mg twice daily, Zoloft 100 mg twice daily, Abilify 5 mg daily, Motrin 800 mg daily, and a multivitamin.

    ALLERGIES: She has no known drug allergies.

    REVIEW OF SYSTEMS: Negative.

    PHYSICAL EXAM: This is a pleasant female in no acute distress. Alert and oriented x 3. HEENT: Normocephalic, atraumatic. Extraocular muscles intact, nonicteric sclerae. Chest is clear to auscultation bilaterally. Cardiovascular is normal sinus rhythm. Abdomen is obese, soft, nontender and nondistended. Extremities show no edema, clubbing or cyanosis.

    ASSESSMENT/PLAN: This is a 34-year-old female with a BMI of 43 who is interested in surgical weight via the gastric bypass as opposed to Lap-Band. Olivia Smith will be asking for a letter of medical necessity from Dr. Andrew Johnson. She will also see my nutritionist and social worker and have an upper endoscopy. Once this is completed, we will submit her to her insurance company for approval."""

input2 = """Olivia Smith was seen in my office for evaluation for elective surgical weight loss on October 6, 2008. Olivia Smith is a 34-year-old female with a BMI of 43. She is 5'6" tall and weighs 267 pounds. She is motivated to attempt surgical weight loss because she has been overweight for over 20 years and wants to have more energy and improve her self-image. She is not only affected physically, but also socially by her weight. When she loses weight she always regains it and she always gains back more weight than she has lost. At one time, she lost 100 pounds and gained the weight back within a year. She has tried numerous commercial weight loss programs including Weight Watcher's for four months in 1992 with 15-pound weight loss, RS for two months in 1990 with six-pound weight loss, Slim Fast for six weeks in 2004 with eight-pound weight loss, an exercise program for two months in 2007 with a five-pound weight loss, Atkin's Diet for three months in 2008 with a ten-pound weight loss, and Dexatrim for one month in 2005 with a five-pound weight loss. She has also tried numerous fat reduction or fad diets. She was on Redux for nine months with a 100-pound weight loss.\n\nPAST MEDICAL HISTORY: She has a history of hypertension and shortness of breath.\n\nPAST SURGICAL HISTORY: Pertinent for cholecystectomy.\n\nPSYCHOLOGICAL HISTORY: Negative.\n\nSOCIAL HISTORY: She is single. She drinks alcohol once a week. She does not smoke.\n\nFAMILY HISTORY: Pertinent for obesity and hypertension.\n\nMEDICATIONS: Include Topamax 100 mg twice daily, Zoloft 100 mg twice daily, Abilify 5 mg daily, Motrin 800 mg daily, and a multivitamin.\n\nALLERGIES: She has no known drug allergies.\n\nREVIEW OF SYSTEMS: Negative.\n\nPHYSICAL EXAM: This is a pleasant female in no acute distress. Alert and oriented x 3. HEENT: Normocephalic, atraumatic. Extraocular muscles intact, nonicteric sclerae. Chest is clear to auscultation bilaterally. Cardiovascular is normal sinus rhythm. Abdomen is obese, soft, nontender and nondistended. Extremities show no edema, clubbing or cyanosis.\n\nASSESSMENT/PLAN: This is a 34-year-old female with a BMI of 43 who is interested in surgical weight via the gastric bypass as opposed to Lap-Band. Olivia Smith will be asking for a letter of medical necessity from Dr. Andrew Johnson. She will also see my nutritionist and social worker and have an upper endoscopy. Once this is completed, we will submit her to her insurance company for approval.
"""

input3 = """
Olivia Smith was seen in my office for evaluation for elective surgical weight loss on October 6, 2008. Olivia Smith is a 34-year-old female with a BMI of 43. She is 5'6" tall and weighs 267 pounds. 
She is motivated to attempt surgical weight loss because she has been overweight for over 20 years and wants to have more energy and improve her self-image. She is not only affected physically, but also socially by her weight. 
When she loses weight she always regains it and she always gains back more weight than she has lost. At one time, she lost 100 pounds and gained the weight back within a year. 
She has tried numerous commercial weight loss programs including Weight Watcher's for four months in 1992 with 15-pound weight loss, RS for two months in 1990 with six-pound weight loss, 
Slim Fast for six weeks in 2004 with eight-pound weight loss, an exercise program for two months in 2007 with a five-pound weight loss, Atkin's Diet for three months in 2008 with a ten-pound weight loss, 
and Dexatrim for one month in 2005 with a five-pound weight loss. She has also tried numerous fat reduction or fad diets. She was on Redux for nine months with a 100-pound weight loss.

PAST MEDICAL HISTORY: She has a history of hypertension and shortness of breath.

PAST SURGICAL HISTORY: Pertinent for cholecystectomy.

PSYCHOLOGICAL HISTORY: Negative.

SOCIAL HISTORY: She is single. She drinks alcohol once a week. She does not smoke.

FAMILY HISTORY: Pertinent for obesity and hypertension.

MEDICATIONS: Include Topamax 100 mg twice daily, Zoloft 100 mg twice daily, Abilify 5 mg daily, Motrin 800 mg daily, and a multivitamin.

ALLERGIES: She has no known drug allergies.

REVIEW OF SYSTEMS: Negative.

PHYSICAL EXAM: This is a pleasant female in no acute distress. Alert and oriented x 3. HEENT: Normocephalic, atraumatic. Extraocular muscles intact, nonicteric sclerae. Chest is clear to auscultation bilaterally. 
Cardiovascular is normal sinus rhythm. Abdomen is obese, soft, nontender and nondistended. Extremities show no edema, clubbing or cyanosis.

ASSESSMENT/PLAN: This is a 34-year-old female with a BMI of 43 who is interested in surgical weight via the gastric bypass as opposed to Lap-Band. Olivia Smith will be asking for a letter of medical necessity from Dr. Andrew Johnson. 
She will also see my nutritionist and social worker and have an upper endoscopy. Once this is completed, we will submit her to her insurance company for approval.
"""

input4 ="""Olivia Smith was seen in my office for evaluation for elective surgical weight loss on October 6, 2008. Olivia Smith is a 34-year-old female with a BMI of 43. She is 5'6" tall and weighs 267 pounds. She is motivated to attempt surgical weight loss because she has been overweight for over 20 years and wants to have more energy and improve her self-image. She is not only affected physically, but also socially by her weight. When she loses weight she always regains it and she always gains back more weight than she has lost. At one time, she lost 100 pounds and gained the weight back within a year. She has tried numerous commercial weight loss programs including Weight Watcher's for four months in 1992 with 15-pound weight loss, RS for two months in 1990 with six-pound weight loss, Slim Fast for six weeks in 2004 with eight-pound weight loss, an exercise program for two months in 2007 with a five-pound weight loss, Atkin's Diet for three months in 2008 with a ten-pound weight loss, and Dexatrim for one month in 2005 with a five-pound weight loss. She has also tried numerous fat reduction or fad diets. She was on Redux for nine months with a 100-pound weight loss.\n\nPAST MEDICAL HISTORY: She has a history of hypertension and shortness of breath.\n\nPAST SURGICAL HISTORY: Pertinent for cholecystectomy.\n\nPSYCHOLOGICAL HISTORY: Negative.\n\nSOCIAL HISTORY: She is single. She drinks alcohol once a week. She does not smoke.\n\nFAMILY HISTORY: Pertinent for obesity and hypertension.\n\nMEDICATIONS: Include Topamax 100 mg twice daily, Zoloft 100 mg twice daily, Abilify 5 mg daily, Motrin 800 mg daily, and a multivitamin.\n\nALLERGIES: She has no known drug allergies.\n\nREVIEW OF SYSTEMS: Negative.\n\nPHYSICAL EXAM: This is a pleasant female in no acute distress. Alert and oriented x 3. HEENT: Normocephalic, atraumatic. Extraocular muscles intact, nonicteric sclerae. Chest is clear to auscultation bilaterally. Cardiovascular is normal sinus rhythm. Abdomen is obese, soft, nontender and nondistended. Extremities show no edema, clubbing or cyanosis.\n\nASSESSMENT/PLAN: This is a 34-year-old female with a BMI of 43 who is interested in surgical weight via the gastric bypass as opposed to Lap-Band. Olivia Smith will be asking for a letter of medical necessity from Dr. Andrew Johnson. She will also see my nutritionist and social worker and have an upper endoscopy. Once this is completed, we will submit her to her insurance company for approval.
"""