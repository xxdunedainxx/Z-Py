from flask_restplus import reqparse
from flask import request
from ...service.helpers.security.JwtAuth import JwtAuth

dev_user="dev_user"

def http_parse(args):
    parse_args = reqparse.RequestParser()
    for arg in args.keys():
        parse_args.add_argument(arg, type=type(args[arg]))
    structure = parse_args.parse_args()
    return structure


def http_parse_simple(args,arg):

    if arg in args.keys():
        return args[arg]
    else:
        return None

def get_page_number(req_args):
    page = http_parse_simple(req_args, 'page')
    if page is not None:
        page = int(page)

    return page

def get_loged_in_user(dev=False):
    token = request.headers.get('X-Authentication')
    if token is None or "":
        return "null"

    user=JwtAuth.decode_auth_token(token)
    if "user_info" in user.info and "email" in user.info["user_info"].keys():
        return f"{user.info['user_info']['source']}\\{user.info['user_info']['email']}"

    if dev is True:
        return dev_user
    else:
        "null"