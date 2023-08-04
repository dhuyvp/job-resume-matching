import json
from googletrans import Translator

class Translate :
    def __init__(self):
        self.keys = ['skills', 'fulltext', 'educations', 'id', 'gpa', 'major', 'school', 'diploma', 'end_time',\
                     'conf_score', 'start_time', 'picklist_major', 'major categories', 'major_categories_detail',\
                     'experiences', 'detail', 'company', 'industry', 'position',\
                     'title', 'description', 'requirements', 'required_skills']

    def is_vietnamese_readable(self, char):
        # Function to check if the character is a Vietnamese readable character
        # along with some common accented characters (including uppercase)
        vietnamese_accents = 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ'
        return 32 <= ord(char) <= 126 or char in vietnamese_accents

    def is_readable(self, text):
        # Function to check if the text contains only readable characters
        if isinstance(text, list):
            return [self.is_readable(item) for item in text]
        elif isinstance(text, dict):
            return {self.is_readable(key): self.is_readable(value) for key, value in text.items()}
        elif isinstance(text, str):
            return ''.join(char for char in text if self.is_vietnamese_readable(char))
        else:
            return text

    def split_text(self, text, max_length):
        # Split the text into chunks with a maximum length
        chunks = []
        current_chunk = ""
        words = text.split()
        for word in words:
            if len(current_chunk) + len(word) + 1 <= max_length:
                current_chunk += " " + word
            else:
                chunks.append(current_chunk.strip())
                current_chunk = word
        if current_chunk:
            chunks.append(current_chunk.strip())
        return chunks

    def translate_text_chunks(self, text_chunks, translator):
        # Translate text chunks and combine them back into a single translated text
        translated_text = ""
        for chunk in text_chunks:
            translated_chunk = ""
            # print('chunk: ', chunk)
            translated_chunk = translator.translate(chunk, src='vi', dest='en').text
            
            if len( translated_chunk ) < 30  and (translated_chunk.lower() in self.keys) :
                translated_text += translated_chunk.lower() + " "
            else :
                translated_text += translated_chunk + " "
        return translated_text.strip()


    def translate_recursive(self, data, translator):
        translated_dict = {}

        if isinstance(data, dict):
            for key, value in data.items():
                translated_key = self.translate_recursive(key, translator)
                translated_value = self.translate_recursive(value, translator)
                translated_dict[translated_key] = translated_value
            return translated_dict
        elif isinstance(data, list):
            return [self.translate_recursive(item, translator) for item in data]
        elif isinstance(data, str):
            # Split text into chunks and translate each chunk
            
            max_chunk_length = 5000  # Adjust this value as needed
            text_chunks = self.split_text(data, max_chunk_length)
            translated_text = self.translate_text_chunks(text_chunks, translator)
            return translated_text
        else:
            return data  # Return other types as-is (int, bool, etc.)

    def translate_json_file_resume(self, input_id):
        try :
            with open('Data/resume/'+ str(input_id) +'.json', 'r') as f:
                data = json.load(f)

        except FileNotFoundError as e :
            print(f"file resume {input_id}.json does not exist")
        else :
            print(f"file resume {input_id}.json was opened successfully.")

            output_file = str(input_id) + '_translated.json'

            translator = Translator()
            preserved_data = self.is_readable(data)
            translated_data = self.translate_recursive(preserved_data, translator)

            with open('Data_Translated/resume/' + output_file, 'w', encoding='utf-8') as file:
                json.dump(translated_data, file, ensure_ascii=False, indent=2)


    def translate_json_file_job(self, input_id):
        try :
            with open('Data/job_description/'+ str(input_id) +'.json', 'r') as f:
                data = json.load(f)

        except FileNotFoundError as e :
            print(f"file job {input_id}.json does not exist")
        else :
            print(f"file job {input_id}.json was opened successfully.")

            output_file = str(input_id) + '_translated.json'

            translator = Translator()
            preserved_data = self.is_readable(data)
            translated_data = self.translate_recursive(preserved_data, translator)

            with open('Data_Translated/job_description/' + output_file, 'w', encoding='utf-8') as file:
                json.dump(translated_data, file, ensure_ascii=False, indent=2)

