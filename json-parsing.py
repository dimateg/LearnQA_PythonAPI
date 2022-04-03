import json

json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'

media = json.loads(json_text)

pars_json = media['messages'][1]['message']
print(pars_json)