from fastapi import HTTPException


class RAGException(HTTPException):
    def __init__(self, detail: str, status_code: int = 500, error_type: str = "UNKNOWN_ERROR"):
        super().__init__(status_code=status_code, detail=detail)
        self.error_type = error_type
