import json
import requests

response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print('response =', response.text)

response_head_test = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": 'HEAD'})
print('response_head_test =', response_head_test.text, 'status_code =', response_head_test.status_code)

response_true = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": 'POST'})
print('response_true =', response_true.text)

parameters_methods_list = [{"method": 'GET'}, {"method": 'POST'}, {"method": 'PUT'}, {"method": 'DELETE'},
                           {"method": 'OPTIONS'}, {"method": 'HEAD'}, {"method": 'PATCH'}]
methods_list = [requests.get, requests.post, requests.put, requests.delete, requests.options, requests.head,
                requests.patch]
url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

for method in methods_list:
    for params in parameters_methods_list:
        param = params['method']
        result = method(url, params=params)
        method_pars = str(method)[10:-23]
        upper_method = str.upper(method_pars)
        key = "success"
        if key in result.text:
            result_s = json.loads(result.text)
            success = result_s['success']
            if param in upper_method:
                if 'GET' in upper_method:
                    if '!' in success:
                        print('param =', param, ',', 'success =', success, ',', 'method =', upper_method, ',',
                              'test true')
                else:
                    if '!' in success:
                        print('param =', param, ',', 'success =', success, ',', 'method =', upper_method, ',',
                              'test false')
        else:
            print('param =', param, ',', result.text, ',', result.status_code, ',', 'method =', upper_method, ',',
                  'test ERROR')
        result = method(url, data=params)
        method_pars = str(method)[10:-23]
        upper_method = str.upper(method_pars)
        key = "success"
        if key in result.text:
            result_s = json.loads(result.text)
            success = result_s['success']
            if param in upper_method:
                if 'GET' in upper_method:
                    if '!' in success:
                        print('data =', param, ',', 'success =', success, ',', 'method =', upper_method, ',',
                              'test false')
                elif '!' in success:
                    print('data =', param, ',', 'success =', success, ',', 'method =', upper_method, ',', 'test true')
            else:
                if '!' in success:
                    print('data =', param, ',', 'success =', success, ',', 'method =', upper_method, ',', 'test false')
        else:
            print('data =', param, ',', result.text, ',', result.status_code, ',', 'method =', upper_method, ',',
                  'test ERROR')
