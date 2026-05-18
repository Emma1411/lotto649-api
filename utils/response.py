from utils.constants import HTTP, MSG

def success(data=None, message=MSG.SUCCESS):
    return {
        "status":  HTTP.OK,
        "message": message,
        "data":    data
    }

def created(data=None, message=MSG.CREATED):
    return {
        "status":  HTTP.CREATED,
        "message": message,
        "data":    data
    }

def error(message=MSG.ERROR, errors=None):
    return {
        "status":  HTTP.ERROR,
        "message": message,
        "errors":  errors
    }

def not_found(message=MSG.NOT_FOUND):
    return {
        "status":  HTTP.NOT_FOUND,
        "message": message,
        "data":    None
    }

def paginate(data, total, page, per_page, message=MSG.SUCCESS):
    return {
        "status":  HTTP.OK,
        "message": message,
        "pagination": {
            "total":    total,
            "page":     page,
            "per_page": per_page,
            "from":     (page - 1) * per_page + 1,
            "to":       (page - 1) * per_page + len(data)
        },
        "data": data
    }