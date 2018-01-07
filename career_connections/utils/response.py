from flask import jsonify

def create_response(data={}, status=None, http_code=200):
    """
    JSON response formater
    """

    response = jsonify(dict(
        data=data,
        status={'message':status}
    ))
    return response, http_code
