import csv 
from math import log2

id_source_with_label_1 = []
actual_mat = [[] for i in range(6000)]
id_source = []

with open('Data/data.csv', 'r') as f:
  reader = csv.reader(f)
  for row in reader:
    if len(row[1]) != 0 and len(row[2]) != 0 and row[1] != "id" and row[11] != "label":
        job_id = int(row[1])
        resume_id = int(row[2])
        if [job_id, resume_id] not in id_source :
            id_source.append([job_id, resume_id])
            label = int(row[11])
            if label == 1 :
                id_source_with_label_1.append([job_id, resume_id])

            actual_mat[job_id].append([round(float(row[9]), 10), resume_id, label])


# print(id_source_with_label_1)

id_source = []
rel_mat = [[] for i in range(6000)]

with open('final_results4.csv', 'r') as f :
    reader = csv.reader(f)
    
    with open('final.csv', 'w') as fb :
        writer = csv.writer(fb)
        writer.writerow(['job_id', 'resume_id', 'skills_score', 'degrees_score', 'majors_score', 'overall_score', 'label'])

        for row in reversed(list(reader)) :
            if row[0] != 'job_id' :
                job_id = int(row[0])
                resume_id = int(row[1])

                if [job_id, resume_id] not in id_source :
                    id_source.append([job_id, resume_id])

                    if [job_id, resume_id] in id_source_with_label_1 :
                        writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], 1])
                        rel_mat[job_id].append([float(row[5]), resume_id, 1])
                    
                    else :
                        writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], 0])
                        rel_mat[job_id].append([round(float(row[5]), 10), resume_id, 0])


def get_ndcg(predict_id, k) :
    if predict_id > k or predict_id < 1:
        return 0
    
    return 1/(log2(1+predict_id))

#########################

with open('ndcg.csv', 'w') as fw :
    writer = csv.writer(fw)
    writer.writerow(['job_id', 'num_resume', 'predict_id','ndcg@1', 'ndcg@3', 'ndcg@5'])

    for job_id in range(4287, 5330) :
        rel_mat[job_id].sort(reverse=True)
        actual_mat[job_id].sort(reverse=True)

        predict_id = -1
        for id in range( len( rel_mat[job_id] ) ):
            if rel_mat[job_id][id][2] == 1 :
                predict_id = id + 1

        ndcg1 = get_ndcg(predict_id, 1)
        ndcg3 = get_ndcg(predict_id, 3)
        ndcg5 = get_ndcg(predict_id, 5)

        writer.writerow([job_id, len(rel_mat[job_id]), predict_id, ndcg1, ndcg3, ndcg5])


# job_id = 5278
# print('predict_id:', predict_id[job_id])
# print('predict:', rel_mat[job_id])
# print('actual:', actual_mat[job_id])