from JobInfoExtract import JobInfoExtract
import json

def extraction():
    degrees_patterns_path = 'Resources/degrees.jsonl'
    majors_patterns_path = 'Resources/majors.jsonl'
    skills_patterns_path = 'Resources/skills.jsonl'
    # Resources/example_job_4287.json
    with open('Resources/example_job_4287.json', 'r') as f:
        job = json.load(f)

    print(job['requirements'], end = '\n\n')


    job_extraction = JobInfoExtract(skills_patterns_path, majors_patterns_path, degrees_patterns_path, job)
    job_extraction = job_extraction.extract_entites(job)

    return job_extraction


if __name__ == '__main__':

    # extraction()

    ### run
    print('extract information: ', extraction() )

