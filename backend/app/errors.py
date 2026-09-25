class ApplicationError(Exception):
    status_code = 400
    code = "application_error"


class ConfigurationError(ApplicationError):
    status_code = 503
    code = "configuration_error"


class AIProviderError(ApplicationError):
    status_code = 502
    code = "ai_provider_error"


class DocumentNotFoundError(ApplicationError):
    status_code = 404
    code = "document_not_found"


class UnsupportedDocumentError(ApplicationError):
    status_code = 415
    code = "unsupported_document"


class EmptyDocumentError(ApplicationError):
    status_code = 422
    code = "empty_document"


class UploadTooLargeError(ApplicationError):
    status_code = 413
    code = "upload_too_large"


class LearnerNotFoundError(ApplicationError):
    status_code = 404
    code = "learner_not_found"


class LearningSessionNotFoundError(ApplicationError):
    status_code = 404
    code = "learning_session_not_found"


class QuestionNotFoundError(ApplicationError):
    status_code = 404
    code = "question_not_found"


class InvalidLearningStateError(ApplicationError):
    status_code = 409
    code = "invalid_learning_state"
