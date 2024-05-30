from urllib import quote
from collections import OrderedDict


def has_query(arg):
    if "?" in arg and len(arg.split("?")[1]) > 2:
        return True
    return False


def encode_parameters(arg):
    url_parts = arg.split("?", 1)
    query_string = url_parts[1]
    params = OrderedDict(param.split("=") for param in query_string.split("&"))
    encoded_pairs = [quote(key) + "=" + quote(value) for key, value in params.items()]
    encoded_query_string = "&".join(encoded_pairs)
    return url_parts[0] + "?" + encoded_query_string


def get_url(arg):
    start_index = arg.find(" ") + 1
    end_index = arg.find("HTTP/") - 1
    return arg[start_index:end_index]


def get_original_url(raw, encoded):
    start_index = raw.find(" ") + 1
    end_index = raw.find("HTTP/") - 1
    updated = raw[:start_index] + encoded + raw[end_index:]
    return updated


TC = [
    "GET /eb948b03-459a-4bce-9319-0c6db2cde7ac?param1=foo bar HTTP/1.1",
    "GET /eb948b03-459a-4bce-9319-0c6db2cde7ac?param1=foo' %)--!@# bar HTTP/1.1",
    "GET /eb948b03-459a-4bce-9319-0c6db2cde7ac?param1=foo' %)--!@# bar&param2=bar test&param3=a b c d HTTP/1.1",
    "GET /eb948b03-459a-4bce-9319-0c6db2cde7ac?a=b HTTP/1.1",
    "GET /eb948b03-459a-4bce-9319-0c6db2cde7ac? HTTP/1.1",
    "GET /eb948b03-459a-4bce-9319-0c6db2cde7ac HTTP/1.1",
]

for _ in TC:
    url = get_url(_)
    print("[clean_url]", url)
    query = has_query(url)
    print("[has_query]", bool(query))
    if bool(query):
        encoded = encode_parameters(url)
        print("[encoded]", encoded)
        updated = get_original_url(_, encoded)
        print("[final]", updated)
    print("")
