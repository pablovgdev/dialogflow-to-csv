import os
import json
from datetime import date


path_to_json = f'{os.getcwd()}/bot/intents'

json_files = [filename for filename in os.listdir(path_to_json)
              if filename.endswith('.json') and filename.startswith('[')
              and 'usersays' not in filename]

output = 'Context;Intent;Training;Responses\n'

for json_file in json_files:
    intent_name = json_file.replace('.json', '')

    responses_path = f'{os.getcwd()}/bot/intents/{json_file}'
    training_path = f'{os.getcwd()}/bot/intents/{intent_name}_usersays_es.json'

    with open(responses_path, 'r', encoding='utf-8') as responses_file:
        response = json.load(responses_file)
        context = response['contexts'][0] if len(
            response['contexts']) else ''
        speech = response['responses'][0]['messages'][0]['speech']
        responses = ''

        if isinstance(speech, list):
            for text in speech:
                text = text.replace('\\n', '\n')
                responses += text + '\n\n\n'
        else:
            responses += speech

        responses = f'"{responses}"'

    training_phrases = ''

    if 'FALLBACK' not in intent_name and 'EVENT' not in intent_name and '.E' not in intent_name:
        with open(training_path, 'r', encoding='utf-8') as training_file:
            training = json.load(training_file)

            for phrase in training:
                training_phrase = ''

                for word in phrase['data']:
                    training_phrase += word['text']

                training_phrases += training_phrase + '\n'

            training_phrases = f'"{training_phrases}"'

    output += f'{context};{intent_name};{training_phrases};{responses}\n'


with open(f'BOT_{date.today()}.csv', 'w', encoding='utf-8') as result_file:
    result_file.writelines(output)
