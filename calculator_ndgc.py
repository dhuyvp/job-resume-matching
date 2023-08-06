import csv 
from math import log2
import numpy as np

def remove_empty_lists(list1):
        new_list = []
        for item in list1:
            if len(item)== 0 or item[0] == '':
                pass 
            else :
                new_list.append(item)
        return new_list

with open('final_results_all-roberta.csv', 'r') as f :
    reader = csv.reader(f)
    
    # with open('final.csv', 'w') as fb :
    #     writer = csv.writer(fb)
    #     writer.writerow(['job_id', 'resume_id', 'skills_score', 'degrees_score', 'majors_score', 'overall_score', 'label'])

    rows = list(reader)
    rows = remove_empty_lists(rows)
    # print(rows[0])
    # print(rows[1])
    # print(rows[2])
    # print(rows[3])


def guess_x1_x2_x3(x1, x2, x3) :
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


    for row in rows :
        if row[0] != 'job_id':
            job_id = int(row[0])
            resume_id = int(row[1])
            skills_score = float(row[2])
            degrees_score = float(row[3])
            majors_score = float(row[4])
            # x1 = 0/9; x2 = 0/14; x3 = 14/14;

            overall_score = x1 * skills_score + x2 * degrees_score + x3 * majors_score

            if [job_id, resume_id] in id_source_with_label_1 :
                rel_mat[job_id].append([overall_score, resume_id, 1]) 
            else :
                rel_mat[job_id].append([overall_score, resume_id, 0]) 

    def get_ndcg(predict_id, k) :
        if predict_id > k or predict_id < 1:
            return 0
        
        return 1/(log2(1+predict_id))

    #########################

    num_job = 0
    ndcg_vec = [0] * 7
    with open('ndcg.csv', 'w') as fw :
        writer = csv.writer(fw)
        writer.writerow(['job_id', 'num_resume', 'predict_id','ndcg@1', 'ndcg@3', 'ndcg@5', 'ndcg@7', 'ndcg@10', 'ndcg@20', 'ndcg@50'])

        for job_id in range(4287, 5330) :
            rel_mat[job_id].sort(reverse=True)
            # actual_mat[job_id].sort(reverse=True)

            predict_id = -1
            for id in range( len( rel_mat[job_id] ) ):
                if rel_mat[job_id][id][2] == 1 :
                    predict_id = id + 1
                    break

            if len( rel_mat[job_id] ) :
                num_job += 1

                ndcg1 = get_ndcg(predict_id, 1)
                ndcg3 = get_ndcg(predict_id, 3)
                ndcg5 = get_ndcg(predict_id, 5)
                ndcg7 = get_ndcg(predict_id, 7)
                ndcg10 = get_ndcg(predict_id, 10)
                ndcg20 = get_ndcg(predict_id, 20)
                ndcg50 = get_ndcg(predict_id, 50)

                ndcg_vec[0] += ndcg1
                ndcg_vec[1] += ndcg3
                ndcg_vec[2] += ndcg5
                ndcg_vec[3] += ndcg7
                ndcg_vec[4] += ndcg10
                ndcg_vec[5] += ndcg20
                ndcg_vec[6] += ndcg50
                
                
                writer.writerow([job_id, len(rel_mat[job_id]), predict_id, ndcg1, ndcg3, ndcg5, ndcg7, ndcg10, ndcg20, ndcg50])



    print('number of jobs:', num_job)
    print('x1 x2 x3:', [x1, x2, x3])
    print('avg ndcg@k with k=[1, 3, 5, 7, 10, 29, 50]: ', np.array(ndcg_vec) / num_job , '\n')

    return float(ndcg_vec[0])

################3

guess_x1_x2_x3(8/10, 1/10, 1/10) # max
guess_x1_x2_x3(6/10, 1/10, 3/10)
guess_x1_x2_x3(1/10, 8/10, 1/10)
