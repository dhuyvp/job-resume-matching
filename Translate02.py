from Translate import Translate

######################################
for id in range(4500, 4750) :
    trans = Translate()
    trans.translate_json_file_job(id)
    trans.translate_json_file_resume(id)
    
    print(f'Done {id}')