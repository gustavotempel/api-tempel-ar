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

    @abc.abstractmethod
    def update(self, id, obj: models.User):
        pass

    @abc.abstractmethod
    def delete(self, id):
        pass


class UserSqlAlchemyQueryEngine(AbstractQueryEngine):
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

    def update(self, id, user):
        pass

    def delete(self, id):
        pass

    @staticmethod
    def _expunge_user(session: Session, user: models.User):
        session.expunge(user)


class ProductSqlAlchemyQueryEngine(AbstractQueryEngine):
    """A query engine that uses the SQLAlchemy ORM."""

    def __init__(self, session_factory: orm.SessionFactory):
        self.session_factory = session_factory

    def search(self):
        with closing(self.session_factory()) as session:
            query = session.query(models.Product)
            result = query.all()
            for product in result:
                self._expunge_product(session, product)
            return result

    def get(self, id):
        with closing(self.session_factory()) as session:
            result = session.query(models.Product).filter_by(product_id=id).one_or_none()
            if result is not None:
                self._expunge_product(session, result)
            return result

    def add(self, product):
        with closing(self.session_factory()) as session:
            session.add(product)
            session.commit()

    def update(self, id, product):
        with closing(self.session_factory()) as session:
            session.query(models.Product).filter_by(product_id=id).update(product)
            session.commit()

    def delete(self, id):
        with closing(self.session_factory()) as session:
            session.query(models.Product).filter_by(product_id=id).delete()
            session.commit()

    @staticmethod
    def _expunge_product(session: Session, product: models.Product):
        session.expunge(product)
