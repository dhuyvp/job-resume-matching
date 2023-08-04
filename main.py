from JobInfoExtract import JobInfoExtract
from Rules import Rules
from dotenv import load_dotenv
import json
import ast
import csv
import os

def extraction(job):
    degrees_patterns_path = 'Resources/degrees.jsonl'
    majors_patterns_path = 'Resources/majors.jsonl'
    skills_patterns_path = 'Resources/skills.jsonl'

    # print(job['requirements'], end = '\n\n')

    job_extraction = JobInfoExtract(skills_patterns_path, majors_patterns_path, degrees_patterns_path, job)
    job_extraction = job_extraction.extract_entites(job)

    return job_extraction

def job_resume_matching(job, resume) :

    pass

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

    except FileNotFoundError as e:
        print(f"file resume {resume_id}.json does not exist")
    else :
        print(f"file resume {resume_id}.json was opened successfully.")

    return resume

def get_score_by_job_resume_id(job_id, resume_id) :
    job = job_source[job_id]
    resume = resume_source[resume_id]


    [skills_score, degrees_score, majors_score] = [0, 0, 0]
    if (job== {}) or (resume == {}) :
        print(f'job {job_id} or resume {resume_id} does not exist\n')
    else :
    
        job_extracted = extraction(job)
        # job_extracted = modifying_type_job(job_extracted)
        # resume = modifying_type_resume(resume)
        rule_object = Rules(resume, job_extracted)
        
        # print('type of resume', type(resume), '\ntype of job:', type(job_extracted))
        
        [skills_score, degrees_score, majors_score] = rule_object.matching_score(resume, job_extracted, job_id)
        print('skills score:', skills_score)
        print('degrees score:', degrees_score)
        print('majors score:', majors_score)
        print('overall score:', (skills_score*2+majors_score+degrees_score)/4)
        print(f'Done job {job_id} or resume {resume_id}\n')


    return [skills_score, degrees_score, majors_score]

if __name__ == '__main__':
    load_dotenv()

    job_source = [{}] * 6000
    for job_id in range(4287, 5330) :
        job_source[job_id] = get_job_by_id(job_id)

    resume_source = [{}] * 6000
    for resume_id in range(4287, 5330) :
        resume_source[resume_id] = get_resume_by_id(resume_id)

    with open('final_results.csv', 'w') as f :
        writer = csv.writer(f)
        writer.writerow(['job_id', 'resume_id', 'skills_score', 'degrees_score', 'overall_score'])

        for job_id in range(4287, 5324) :
            for resume_id in range(4287, 5324) :
                [skills_score, degrees_score, majors_score] = get_score_by_job_resume_id(job_id, resume_id) 
                if [skills_score, degrees_score, majors_score] == [0, 0, 0] :
                    pass 
                else :
                    writer.writerow([job_id, resume_id, skills_score, degrees_score, majors_score, (skills_score*2+majors_score+degrees_score)/4])
