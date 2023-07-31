import ast
import json
from Resources import DEGREES_IMPORTANCE
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class Rules:
    def __init__(self, resumes, jobs):
        with open('Resources/labels.json') as fp:
            labels = json.load(fp)

        self.labels = labels
        self.resumes = resumes
        self.jobs = jobs
        self.degrees_importance = DEGREES_IMPORTANCE

    def modifying_type_resume(self, resumes) :
        resumes['skills'] = ast.literal_eval(resumes['skills'])

        return resumes

    def modifying_type_job(self, jobs) :
        jobs['Skills'] = ast.literal_eval(jobs['Skills'])

        return jobs
    
    # skills matching
    @staticmethod
    def unique_job_skills(job) :
        unique_job_skills = []
        for i in job['Skills'] :
            if i not in unique_job_skills :
                unique_job_skills.append(i)

        return unique_job_skills

    def semantic_similarity(self, job, resume):
        model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
        # model = SentenceTransformer('xlm-roberta-large')

        score = 0
        sen = job + resume

        print('\n\njob before encode: ', job)
        print('\nresume before encode: ', resume)

        
        sen_embeddings = model.encode(sen)
        print('\n\n\nsen:', sen, '\n\n\n')
        print('\n\n\nsen_embeddings:', sen_embeddings.shape, '\n\n\n')
        
        for i in range(len(job)) :
            if job[i] in resume : 
                score += 1
            else :
                if max(cosine_similarity([sen_embeddings[i]], sen_embeddings[len(job):])[0]) >= 0.4 :
                    score += max(cosine_similarity([sen_embeddings[i]], sen_embeddings[len(job):])[0])

        score = score / len(job)
        return round(score, 6)


    def skills_semantic_matching(self, resume, job_index, job_skills) :
        resume['Skills job ' + str(job_index) + ' semantic matching'] = 0
        
        resume['Skills job ' + str(job_index) + ' semantic matching'] = self.semantic_similarity(job_skills, resume['skills'])

        return resume

    # calculate matching scores
    def matching_score(self, resume, job, job_index):
        print('type matching resume:', type(resume), '\n\n')
        print('matching resume:', resume, '\n\n')

        job_skills = self.unique_job_skills(job)
        resume = self.skills_semantic_matching(resume, job_index, job_skills)

        skills_score = 0 \
            + resume['Skills job ' + str(job_index) + ' semantic matching']

        return skills_score
    

#############################################################
