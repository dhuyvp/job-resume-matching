from JobInfoExtract import JobInfoExtract
from Rules import Rules
import json
import ast

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


if __name__ == '__main__':
    # Resources/example_job_4287.json
    # with open('Resources/example_job_4287.json', 'r') as f:
    #     job = json.load(f)
    
    # with open('Resources/example_resume_5254.json', 'r') as f:
    #     resume = json.load(f)

    with open('Data/job_description/4288.json', 'r') as f:
        job = json.load(f)

    with open('Data/resume/4288.json', 'r') as f:
        resume = json.load(f)
    

    with open('Resources/labels.json') as fp:
        labels = json.load(fp)

    job_extracted = extraction(job)
    # job_extracted = modifying_type_job(job_extracted)
    # resume = modifying_type_resume(resume)

    print('----------------------------\n')
    print(job_extracted)
    print('----------------------------\n')
    print(resume)
    


    rule_object = Rules(labels, resume, job_extracted)
    
    print('type of resume', type(resume), '\ntype of job:', type(job_extracted))
    
    skills_score = rule_object.matching_score(resume, job_extracted, 0)
    print('skills score:', skills_score)

    # print(job_extracted)



    pass