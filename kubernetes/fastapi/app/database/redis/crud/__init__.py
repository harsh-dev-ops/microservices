from .tokens import TokenCrud


def get(cls_name:str):
    obj = dict(token_crud=TokenCrud())
    return obj[cls_name]
    