# Bài tập 1 #

class ApiError(Exception): # loi của api
    status_code = 500
    code = "internal_error"

    def __init__(self, message="", code=None, status=None):
        super().__init__(message)
        self.message = message
        if code: self.code = code
        if status: self.status_code = status

class NotFound(ApiError):
    status_code = 404
    code = "not_found"

class Conflict(ApiError):
    status_code = 409
    code = "conflict"

class OutOfStock(ApiError): # lỗi khi hết hàng
    status_code = 409
    code = "out_of_stock"