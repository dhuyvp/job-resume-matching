from JobInfoExtract import JobInfoExtract
from Rules import Rules
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import json
import ast
import csv
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from preprocessing_function import CustomPreprocess
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("sentence-transformers/all-roberta-large-v1")
custom_prepreocess = CustomPreprocess()
def extraction(job):
    degrees_patterns_path = 'Resources/degrees.jsonl'
    majors_patterns_path = 'Resources/majors.jsonl'
    skills_patterns_path = 'Resources/skills.jsonl'

    # print(job['requirements'], end = '\n\n')

    job_extraction = JobInfoExtract(skills_patterns_path, majors_patterns_path, degrees_patterns_path, job)
    job_extraction = job_extraction.extract_entites(job)

    return job_extraction

def modifying_type_resume(resumes):
    # for i in range(len(resumes["degrees"])):
    #     resumes["degrees"][i] = ast.literal_eval(resumes["degrees"][i])
    # for i in range(len(resumes["skills"])):
    resumes["skills"]= ast.literal_eval(resumes["skills"])
    return resumes


def modifying_type_job(jobs):
    # for i in range(len(jobs["Skills"])):
    jobs["Skills"] = ast.literal_eval(jobs["Skills"])
    return jobs

def get_job_by_id(job_id) :
    job = {}
    try :
        with open('Data_Translated/job_description/'+ str(job_id) +'_translated.json', 'r') as f:
            job = json.load(f)
            job = extraction(job)

            job['Skills'] = [ ', '.join( [ele for ele in job['Skills'] ] ) ]
            job['Skills'] = model.encode(job['Skills'])

            #new
            if job['requirements'] is None : 
                job['jacard'] = ''
            else :
                job['jacard'] = job['requirements']
            
            if job['description'] is None : 
                job['jacard'] += ''
            else :
                job['jacard'] +=' ' + job['description']
            
            job['jacard'] = [ custom_prepreocess.preprocess_text(job['jacard']) ]
            job['jacard'] = model.encode(job['jacard'])
            # print(tokens)
            job['title'] = model.encode([ job['title'] ] )

    except FileNotFoundError as e:
        print(f"file job {job_id}.json does not exist")
    else :
        print(f"file job {job_id}.json was opened successfully.")

    return job

def get_resume_by_id(resume_id) :
    resume = {}
    try :
        with open('Data_Translated/resume/'+ str(resume_id) +'_translated.json', 'r') as f:
            resume = json.load(f)

            resume['skills'] = [ ', '.join( [ele for ele in resume['skills'] ] ) ]
            resume['skills'] = model.encode(resume['skills'])

            #new 
            if resume['fulltext'] is None :
                resume['jacard'] = ''
            else :
                resume['jacard'] = resume['fulltext']
            resume['jacard'] = [ custom_prepreocess.preprocess_text(resume['jacard']) ]
            resume['jacard'] = model.encode(resume['jacard'])
            # print(resume['jacard'])

            resume_majors = []
            for edu in resume['educations'] :
                if (edu['major']) is not None :
                    resume_majors.append(edu['major'])
            resume['majors'] = resume_majors
            resume['majors_encode'] = [', '.join(  [ele for ele in resume['majors'] ] )]
            resume['majors_encode'] = model.encode(resume['majors_encode']) # using to compare title in job

    except FileNotFoundError as e:
        print(f"file resume {resume_id}.json does not exist")
    else :
        print(f"file resume {resume_id}.json was opened successfully.")

    return resume
###############
def get_jacard_score(job_id, resume_id) :
    job = get_job_by_id(job_id)
    resume = get_resume_by_id(resume_id)

    print(job['title'].shape, resume['majors_encode'].shape)
    print(job['title'])
    print(resume['majors_encode'])
    print( cosine_similarity(job['title'], resume['majors_encode']) )

#############3
def get_score_by_job_resume_id(job_id, resume_id) :
    job = job_source[job_id]
    resume = resume_source[resume_id]


    [skills_score, degrees_score, majors_score] = [0, 0, 0]
    if (job== {}) or (resume == {}) :
        print(f'job {job_id} or resume {resume_id} does not exist\n')
    else :
        # job_extracted = job
        # job_extracted = extraction(job)
        # job_extracted = modifying_type_job(job_extracted)
        # resume = modifying_type_resume(resume)
        rule_object = Rules(resume, job)
        
        # print('type of resume', type(resume), '\ntype of job:', type(job_extracted))
        
        [skills_score, degrees_score, majors_score] = rule_object.matching_score(resume, job, job_id)
        [jacard_score, title_score] = rule_object.bonus_score(resume, job)
        # print('skills score:', skills_score)
        # print('degrees score:', degrees_score)
        # print('majors score:', majors_score)
        # print('overall score:', (skills_score*2+majors_score+degrees_score)/4)
        print(f'Done job {job_id} and resume {resume_id}\n')


    return [skills_score, degrees_score, majors_score, jacard_score, title_score]

if __name__ == '__main__':
    # load_dotenv()

    job_source = [{}] * 6000
    for job_id in range(4287, 5323) :
        job_source[job_id] = get_job_by_id(job_id)

    resume_source = [{}] * 6000
    for resume_id in range(4287, 5323) :
        resume_source[resume_id] = get_resume_by_id(resume_id)

    with open('final_results.csv', 'w') as f :
        writer = csv.writer(f)
        writer.writerow(['job_id', 'resume_id', 'skills_score', 'degrees_score', 'majors_score', 'jacard_score', 'title_score', 'overall_score'])

        for job_id in range(4287, 5323) :
            for resume_id in range(4287, 5323) :
                [skills_score, degrees_score, majors_score, jacard_score, title_score] = get_score_by_job_resume_id(job_id, resume_id) 
                if [skills_score, degrees_score, majors_score, jacard_score, title_score] == [0, 0, 0, 0, 0] :
                    pass 
                else :
                    writer.writerow([job_id, resume_id, skills_score, degrees_score, majors_score, jacard_score, title_score, \
                                     (skills_score*2+majors_score+degrees_score+jacard_score*2+title_score)/7])



    # get_jacard_score(4287, 4287)