from sqlalchemy import Table, Column, create_engine, insert, delete, text, select, update
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, ForeignKey, String, Unicode, Numeric, Boolean, DateTime, TIMESTAMP, MetaData
import sqlalchemy.ext.declarative
from sqlalchemy.orm import backref, relation
from sqlalchemy.exc import ArgumentError
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
import json
import random
import string
import datetime

DeclarativeBase = sqlalchemy.ext.declarative.declarative_base()
metadata = DeclarativeBase.metadata
DATABASE_URI = 'postgresql://postgres:14725@localhost:5433/db2'
engine = create_engine(DATABASE_URI)
class Person(DeclarativeBase):
    __tablename__ = 'person'

    pid = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    exemption = Column(String)

class Transport(DeclarativeBase):
    __tablename__ = 'transport'

    car_number = Column(Integer, primary_key=True)
    route_number = Column(Integer)

class Stop:
    __tablename__ = 'stop'

    sid = Column(Integer, primary_key=True)
    address = Column(String)

class Ticket:
    __tablename__ = 'ticket'

    tid = Column(Integer, primary_key=True)
    price = Column(Numeric)
    operation_time = Column(DateTime)

class Schedule:
    __tablename__ = 'schedule'

    schedule_id  = Column(Integer, primary_key=True)
    car_number = Column("car_number", Integer, ForeignKey("transport.car_number", ondelete="CASCADE"))
    sid = Column("sid", Integer, ForeignKey("stop.sid", ondelete="CASCADE"))
    time = Column(DateTime)

class Ownership:
    __tablename__ = 'ownership'

    tid = Column("tid", Integer, ForeignKey("ticket.tid", ondelete="CASCADE"), primary_key=True)
    pid = Column("pid", Integer, ForeignKey('person.pid', ondelete="CASCADE"))

class Trip:
    __tablename__ = 'tripid'

    tripid = Column("tripid", Integer, primary_key=True)
    car_number = Column("car_number", Integer, ForeignKey("transport.car_number", ondelete="CASCADE"))
    tid = Column("tid", Integer, ForeignKey("ticket.tid", ondelete="CASCADE"))
    start_time = Column("start_time", DateTime)
    end_time = Column('end_time', DateTime)

DeclarativeBase.metadata.create_all(engine)


def output(filename, data):
        with open(filename, 'w+') as f:
            f.writelines("%s\n" % place for place in data)


class Database:

    def __init__(self):
        try:
            DATABASE_URI = 'postgresql://adniry:14725@localhost:5432/db2'
            self.engine = create_engine(DATABASE_URI)
            #self.engine = create_engine('postgresql://postgres:6969@localhost:5433/postgres')
            self.metadata = MetaData() #DeclarativeBase.metadata
            self.metadata.reflect(self.engine)
            self.base = automap_base(metadata=self.metadata)
            self.base.prepare()
            session_class = sessionmaker(bind=self.engine)

            self.session = session_class()


        except ArgumentError:
            print('Argument error')

    def delete_all(self):
        """
        It deletes all items and all lists
        """
        self.session.query(self.base.classes['person']).delete()
        self.session.query(self.base.classes['ticket']).delete()
        self.session.query(self.base.classes['stop']).delete()
        self.session.query(self.base.classes['schedule']).delete()
        self.session.query(self.base.classes['ownership']).delete()
        self.session.query(self.base.classes['trip']).delete()
        self.session.query(self.base.classes['transport']).delete()
        self.session.commit()

    def save_all(self, objects):
        """
        It commits objects created by outer scope
        :param objects: a list of objects to save
        """
        self.session.add_all(objects)
        self.session.commit()

    def delete_request(self, table, where):
        '''
        deletes the row with condition where
        :param table: name of the table
        :param where: condition to delete
        :return:
        '''
        temp = Table(table, self.metadata, autoload=True, autoload_with=self.engine)
        query = delete(temp).where(text(str(where)))
        results = self.session.execute(query)
        results = self.session.execute(select([temp])).fetchall()
        output('output.txt', results)
        self.session.commit()

    def insert_request(self, table, condition):
        temp = Table(table, self.metadata, autoload=True, autoload_with=self.engine)
        res = eval('dict(' + condition + ')')
        query = insert(temp)
        ResultProxy = self.session.execute(query, res)
        results = self.session.execute(select([temp])).fetchall()
        output('output.txt', results)
        self.session.commit()

    def update_request(self, table, condition):
        temp = Table(table, self.metadata, autoload=True, autoload_with=self.engine)
        where, what = condition.split(',')
        res = eval('dict(' + what + ')')
        query = update(temp).values(res).where(text(where))
        results = self.session.execute(query)
        results = self.session.execute(select([temp])).fetchall()
        output('output.txt', results)
        self.session.commit()

    def requestFormat(self, comboTable, comboAction, textAction, Controller):
        Controller.gen_label.setText('')

        if comboAction == 'delete':
            try:
                self.delete_request(comboTable, textAction)
                Controller.error.setText('Done')

            except Exception as error:
                session_class = sessionmaker(bind=self.engine)
                self.session = session_class()
                Controller.error.setText(str(error))
        elif comboAction == 'insert':
            try:
                self.insert_request(comboTable, textAction)
                Controller.error.setText('Done')

            except Exception as error:
                session_class = sessionmaker(bind=self.engine)
                self.session = session_class()
                Controller.error.setText(str(error))
        elif comboAction == 'update':
            try:
                self.update_request(comboTable, textAction)
                Controller.error.setText('Done')

            except Exception as error:
                session_class = sessionmaker(bind=self.engine)
                self.session = session_class()
                Controller.error.setText(str(error))

