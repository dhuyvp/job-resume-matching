from JobInfoExtract import JobInfoExtract
from Rules import Rules
import json
import ast
import csv

def extraction(job):
    degrees_patterns_path = 'Resources/degrees.jsonl'
    majors_patterns_path = 'Resources/majors.jsonl'
    skills_patterns_path = 'Resources/skills.jsonl'

    print(job['requirements'], end = '\n\n')

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
    with open('Data/job_description/'+ str(job_id) +'.json', 'r') as f:
        job = json.load(f)
    return job

def get_resume_by_id(resume_id) :
    with open('Data/resume/'+ str(resume_id) +'.json', 'r') as f:
        resume = json.load(f)
    return resume

def get_score_by_job_resume_id(job_id, resume_id) :
    job = get_job_by_id(job_id)
    resume = get_resume_by_id(resume_id)
    
    job_extracted = extraction(job)
    # job_extracted = modifying_type_job(job_extracted)
    # resume = modifying_type_resume(resume)

    # print('----------------------------\n')
    # print(job_extracted)
    # print('----------------------------\n')
    # print(resume)
    
    rule_object = Rules(resume, job_extracted)
    
    # print('type of resume', type(resume), '\ntype of job:', type(job_extracted))
    
    skills_score = rule_object.matching_score(resume, job_extracted, 0)
    print('skills score:', skills_score)

    return skills_score

if __name__ == '__main__':
    
    with open('final_results.csv', 'w') as f :
        writer = csv.writer(f)
        writer.writerow(['job_id', 'resume_id', 'skills_score'])

        for id in range(4287, 4600) : 
            writer.writerow([id, id, get_score_by_job_resume_id(id, id)])

    