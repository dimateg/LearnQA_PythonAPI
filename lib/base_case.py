import json.decoder

from requests import Response
class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Не найден куки для имени {cookie_name} в последнем запросе"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, header_name):
        assert header_name in response.headers, f"Не найден куки для имени {header_name} в последнем запросе"
        return response.headers[header_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecoder:
            assert False, f"Ответ находится не в JSON фотрмате. Response text is {response.text}"

        assert name in response_as_dict, f"Ответ в JSON не имеет ключа {name}"

        return response_as_dict[name]