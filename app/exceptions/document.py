class DocLensException(Exception):
    pass


class DocumentCreationError(DocLensException):
    pass

class DocumentNotFoundError(DocLensException):
    pass

class DocumentStatusUpdateError(DocLensException):
    pass

class DocumentDeletionError(DocLensException):
    pass

class OcrError(DocLensException):
    pass
