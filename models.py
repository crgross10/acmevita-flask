from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///acmevita.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class Departamentos(Base):
    __tablename__='departamentos'
    id = Column(Integer, primary_key=True)
    departamento = Column(String(50), index=True)

    def __repr__(self):
        return '<Departamento {}>'.format(self.nome)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

class Colaboradores(Base):
    __tablename__='colaboradores'
    id = Column(Integer, primary_key=True)
    nome_completo = Column(String(80))
    departamento_id = Column(Integer, ForeignKey('departamentos.id'))
    departamento = relationship("Departamentos")

    def __repr__(self):
        return '<Colaborador {}>'.format(self.nome)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

class Dependentes(Base):
    __tablename__='dependentes'
    id = Column(Integer, primary_key=True)
    nome_completo = Column(String(100))
    colaborador_id = Column(Integer, ForeignKey('colaboradores.id'))
    colaborador = relationship("Colaboradores")

    def __repr__(self):
        return '<Dependente {}>'.format(self.login)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()
