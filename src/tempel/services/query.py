import abc
from contextlib import closing

from sqlalchemy.orm import Session

from tempel.adapters import orm
from tempel.domain import models


class AbstractQueryEngine(abc.ABC):
    """A proxy for queries against the persistance layer."""

    @abc.abstractmethod
    def search(self):
        pass

    @abc.abstractmethod
    def get(self, id):
        pass

    @abc.abstractmethod
    def add(self, obj: models.User):
        pass


class SqlAlchemyQueryEngine(AbstractQueryEngine):
    """A query engine that uses the SQLAlchemy ORM."""

    def __init__(self, session_factory: orm.SessionFactory):
        self.session_factory = session_factory

    def search(self):
        with closing(self.session_factory()) as session:
            query = session.query(models.User)
            result = query.all()
            for user in result:
                self._expunge_user(session, user)
            return result

    def get(self, id):
        with closing(self.session_factory()) as session:
            result = session.query(models.User).filter_by(user_id=id).one_or_none()
            if result is not None:
                self._expunge_user(session, result)
            return result

    def add(self, user):
        with closing(self.session_factory()) as session:
            session.add(user)
            session.commit()
            print(user)

    @staticmethod
    def _expunge_user(session: Session, user: models.User):
        session.expunge(user)
