class HTTP_STATUS_CODE():
    def __init__(self):
        msg = {500: 'INTERNAL_SERVER_ERROR', 501: 'NOT_IMPLEMENTED', 502: 'BAD_GATEWAY', 503: 'SERVICE_UNAVAILABLE',
               504: 'GATEWAY_TIMEOUT',
               505: 'HTTP_VERSION_NOT_SUPPORTED', 511: 'NETWORK_AUTHENTICATION_REQUIRED', 400: 'BAD_REQUEST',
               401: 'UNAUTHORIZED',
               402: 'PAYMENT_REQUIRED', 403: 'FORBIDDEN', 404: 'NOT_FOUND', 405: 'METHOD_NOT_ALLOWED',
               406: 'NOT_ACCEPTABLE',
               407: 'PROXY_AUTHENTICATION_REQUIRED', 408: 'REQUEST_TIMEOUT', 409: 'CONFLICT', 410: 'GONE',
               411: 'LENGTH_REQUIRED',
               412: 'PRECONDITION_FAILED', 413: 'REQUEST_ENTITY_TOO_LARGE', 414: 'REQUEST_URI_TOO_LONG',
               415: 'UNSUPPORTED_MEDIA_TYPE',
               416: 'REQUESTED_RANGE_NOT_SATISFIABLE', 417: 'EXPECTATION_FAILED', 428: 'PRECONDITION_REQUIRED',
               429: 'TOO_MANY_REQUESTS',
               431: 'REQUEST_HEADER_FIELDS_TOO_LARGE', 100: 'CONTINUE', 101: 'SWITCHING_PROTOCOLS',
               300: 'MULTIPLE_CHOICES',
               301: 'MOVED_PERMANENTLY', 302: 'FOUND', 302: 'SEE_OTHER', 304: 'NOT_MODIFIED', 305: 'USE_PROXY',
               306: 'RESERVED', 307: 'TEMPORARY_REDIRECT'}

    def get_msg(self, code):
        if code in self.msg.keys:
            return self.msg[code]