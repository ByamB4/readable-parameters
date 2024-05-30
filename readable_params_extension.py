from burp import IBurpExtender, IHttpListener
from urllib import quote
from collections import OrderedDict


class BurpExtender(IBurpExtender, IHttpListener):

    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()

        callbacks.setExtensionName("Readable Params Extension")
        callbacks.registerHttpListener(self)

        print("[success] Extension loaded")

    def get_response_detail(self, content):
        response = content.getResponse()
        response_data = self._helpers.analyzeResponse(response)
        headers = list(response_data.getHeaders())
        body = response[response_data.getBodyOffset() :].tostring()
        return headers, body

    def get_request_detail(self, content):
        request = content.getRequest()
        request_data = self._helpers.analyzeRequest(request)
        method = request_data.getMethod()
        headers = list(request_data.getHeaders())
        body = request[request_data.getBodyOffset() :].tostring()
        return headers, body, method

    def has_query(self, arg):
        if "?" in arg and len(arg.split("?")[1]) > 2:
            return True
        return False

    def encode_parameters(self, arg):
        url_parts = arg.split("?", 1)
        query_string = url_parts[1]
        params = OrderedDict(param.split("=") for param in query_string.split("&"))
        encoded_pairs = [quote(key) + "=" + quote(value) for key, value in params.items()]
        encoded_query_string = "&".join(encoded_pairs)
        return url_parts[0] + "?" + encoded_query_string

    def get_url(self, arg):
        start_index = arg.find(" ") + 1
        end_index = arg.find("HTTP/") - 1
        return arg[start_index:end_index]

    def get_original_url(self, raw, encoded):
        start_index = raw.find(" ") + 1
        end_index = raw.find("HTTP/") - 1
        updated = raw[:start_index] + encoded + raw[end_index:]
        return updated

    def processHttpMessage(self, tool, is_request, content):
        if is_request and tool == self._callbacks.TOOL_REPEATER:
            headers, body, method = self.get_request_detail(content)
            url = self.get_url(headers[0])
            if self.has_query(url):
                encoded = self.encode_parameters(url)
                updated = self.get_original_url(headers[0], encoded)
                new_header = [updated]
                for i in range(1, len(headers)):
                    new_header.append(headers[i])
                new_request = self._helpers.buildHttpMessage(new_header, body)
                content.setRequest(new_request)
                print("[updated]", updated)
            else:
                print("[debug] no parameter")
