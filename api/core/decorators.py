from functools import wraps
from sqlalchemy.exc import (
    IntegrityError,
    OperationalError,
    DatabaseError,
    DataError,
    ProgrammingError,
    InvalidRequestError,
    InterfaceError,
    TimeoutError,
    NoResultFound,
    MultipleResultsFound,
    SQLAlchemyError,
)
from sqlalchemy.orm import Session
from api.core.exceptions import (
    ExceptionBadRequest,
    ExceptionConflict,
    ExceptionNotFound,
    ExceptionInternalServerError,
    ExceptionInvalidData,
    ExceptionForbidden
)

def handle_sqlalchemy_errors(func):
    @wraps(func)
    def wrapper(self, db: Session, *args, **kwargs):
        try:
            return func(self, db, *args, **kwargs)
        except IntegrityError as e:
            db.rollback()
            raise ExceptionInvalidData(detail=f"Erro de integridade: {str(e.orig)}")
        except OperationalError as e:
            db.rollback()
            raise ExceptionInternalServerError(detail=f"Erro de conexão com o banco de dados: {str(e)}")
        except DatabaseError as e:
            db.rollback()
            raise ExceptionInternalServerError(detail=f"Erro no banco de dados: {str(e)}")
        except DataError as e:
            db.rollback()
            raise ExceptionInvalidData(detail=f"Erro de dados: {str(e)}")
        except ProgrammingError as e:
            db.rollback()
            raise ExceptionInternalServerError(detail=f"Erro de sintaxe: {str(e)}")
        except InvalidRequestError as e:
            db.rollback()
            raise ExceptionBadRequest(detail="Erro de solicitação inválida")
        except InterfaceError as e:
            db.rollback()
            raise ExceptionInternalServerError(detail=f"Erro de interface: {str(e)}")
        except TimeoutError as e:
            db.rollback()
            raise ExceptionInternalServerError(detail=f"Erro de timeout: {str(e)}")
        except NoResultFound as e:
            db.rollback()
            raise ExceptionNotFound(detail="Nenhum resultado encontrado")
        except MultipleResultsFound as e:
            db.rollback()
            raise ExceptionBadRequest(detail=f"Múltiplos resultados encontrados: {str(e)}")
        except SQLAlchemyError as e:
            db.rollback()
            raise ExceptionInternalServerError(detail=f"Erro no SQLAlchemy: {str(e)}")
        # Exceções personalizadas propagadas diretamente
        except (ExceptionBadRequest, ExceptionNotFound, ExceptionInvalidData, ExceptionConflict, ExceptionForbidden) as e:
            raise e
        except Exception as e:
            db.rollback()
            raise ExceptionInternalServerError(detail=f"Erro interno: {str(e)}")
    return wrapper
