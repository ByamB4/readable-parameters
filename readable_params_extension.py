from burp import IBurpExtender, IHttpListener

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

    def processHttpMessage(self, tool, is_request, content):
        if is_request and tool == self._callbacks.TOOL_REPEATER:
            headers, body, method = self.get_request_detail(content)
            if '?' in headers[0]:
                start_index = headers[0].find('?')+1
                end_index = headers[0].find('HTTP/')-1
                parameters = headers[0][start_index:end_index].split('&')
                for param in parameters:
                    _key, _value = param.split('=')
                    print('_key', _key)
                    print('_value', _value)

            # new_header = []
            # for header in headersheaders:
            #     if 'If-None-Match: ' in header:
            #         print('[debug] If-None-Match ' + str(headers[0]))
            #     elif 'If-Modified-Since:' in header:
            #         print('[debug] If-Modified-Match ' + str(headers[0]))
            #     else:
            #         new_header.append(header)
            # new_request = self._helpers.buildHttpMessage(new_header, body)
            # content.setRequest(new_request)
