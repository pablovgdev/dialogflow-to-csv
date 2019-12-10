import os
import json
from datetime import date


path_to_json = f'{os.getcwd()}/bot/intents'

json_files = [filename for filename in os.listdir(path_to_json)
              if filename.endswith('.json') and filename.startswith('[')
              and 'usersays' not in filename]

output = 'Context\tIntent\tResponses\n'

for json_file in json_files:
    intent_name = json_file.replace('.json', '')

    responses_path = f'{os.getcwd()}/bot/intents/{json_file}'
    training_path = f'{os.getcwd()}/bot/intents/{intent_name}_usersays_es.json'

    with open(responses_path, 'r', encoding='utf-8') as responses_file:
        response = json.load(responses_file)
        context = response['contexts'][0] if len(
            response['contexts']) else 'GLOBAL'
        speech = response['responses'][0]['messages'][0]['speech']
        responses = ''

        if isinstance(speech, list):
            for text in speech:
                text = text.replace('\\n', '\n')
                responses += text + '\n\n\n'
        else:
            responses += speech

        responses = f'"{responses}"'

    output += f'{context}\t{intent_name}\t{responses}\n'


with open(f'BOT_RESPONSES{date.today()}.tsv', 'w', encoding='utf-8') as result_file:
    result_file.writelines(output)
