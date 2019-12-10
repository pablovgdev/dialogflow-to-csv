import json
import os
from datetime import date

path_to_json = f'{os.getcwd()}/bot/intents'

json_files = [filename for filename in os.listdir(path_to_json)
              if filename.endswith('.json') and filename.startswith('[')
              and 'usersays' not in filename]

output = {}

for json_file in json_files:
    intent = json_file.replace('.json', '')

    intent_position, intent_name = intent.split(' ')
    intent_position = intent_position.replace('[', '').replace(']', '')

    responses_path = f'{os.getcwd()}/bot/intents/{json_file}'

    with open(responses_path, 'r', encoding='utf-8') as responses_file:
        response = json.load(responses_file)
        speech = response['responses'][0]['messages'][0]['speech']
        responses = []

        if isinstance(speech, list):
            for text in speech:
                text = text.replace('\\n', '\n')
                responses.append(text)
        else:
            responses.append(speech)

    output[intent_position] = {'name': intent_name, 'responses': responses}

with open(f'BOT_RESPONSES_{date.today()}.json', 'w', encoding='utf-8') as result_file:
    json.dump(output, result_file, ensure_ascii=False)
