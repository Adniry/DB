import psycopg2 as ps
from configparser import ConfigParser
import datetime
from datetime import timedelta
import json

class Database:

    def config(self, filename='config.ini', section='postgresql'):
        parser = ConfigParser()
        parser.read(filename)
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))
        return db

    def get_request(self, req):
        try:
            cursor = self.conn.cursor()
            cursor.execute(req)
            self.conn.commit()
            self.colnames = [desc[0] for desc in cursor.description]
            return cursor.fetchall()
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            self.conn.rollback()
            self.gen_error = error
            self.erFlag = True
            print(error)
            return False

    def __init__(self):
        self.conn = None
        self.error = ''
        self.gen_error = ''
        self.erFlag = False
        self.Gen = True
        self.colnames = list()
        try:
            params = self.config('config.ini')
            self.conn = ps.connect(**params)

        except(Exception, ps.DatabaseError) as error:
            print(error)

    def delete_request(self, action, text):
        return self.request("DELETE FROM {0} WHERE {1};".format(action, text))

    def insert_request(self, table, text):
        enter = [list.split('=') for list in text.split(',')] #devided values
        values = arguments = str()
        for word in enter:
            arguments += word[0] + ','
            values += word[1] + ','
        arguments = arguments[:-1]
        values = values[:-1]
        return self.request("INSERT INTO {0} ({1}) VALUES ({2}) ".format(table, arguments, values))

    def request(self, req):
        try:
            cursor = self.conn.cursor()
            print(req)
            cursor.execute(req)
            cursor.execute("SELECT * FROM person LIMIT 1;")
            self.colnames = [desc[0] for desc in cursor.description]
            self.conn.commit()
            return True
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            print(error)
            self.error = error
            self.conn.rollback()
            return False

    def getValues(self, Cargo):
        from_range = Cargo.textEdit.toPlainText()
        to_range = Cargo.textEdit_2.toPlainText()
        checked = str(not Cargo.checkBox.checkState()==0).lower()
        req = "SELECT * FROM (SELECT * FROM (SELECT * FROM trip RIGHT JOIN ownership ON trip.tid = ownership.tid) AS result WHERE (start_time BETWEEN '{0}' AND '{1}')) AS result  INNER JOIN person ON result.pid = person.pid;".format(from_range, to_range)
        result = self.get_request(req)
        r_str = ""
        for i in result:
            for st in i:
                r_str += str(st) + "    "
            r_str += "\n"
        for word in self.colnames:
            Cargo.columns += word + "\t"
        Cargo.columns += '\n'
        Cargo.plainTextEdit.setPlainText(Cargo.columns + r_str)

    def update_request(self, table, text):
        property = text.split('\n')
        print(property)
        print("UPDATE {0} SET {1} WHERE {2}".format(table, property[1], property[0]))
        return self.request("UPDATE {0} SET {1} WHERE {2}".format(table, property[1], property[0]))

    def generate_values(self):
        with open('data.json', 'r+') as f:
            data = json.load(f)
        self.Gen = False
        start_last_number = data['last_number']+1
        start_estimated_value = data['estimated_value']+1
        amount = 20
        self.Gen= self.request("INSERT INTO person (pid, name, surname, exemption) VALUES (generate_series({0}, {1}), random_string(6), random_string(9), 'pensioner');".format(start_estimated_value, start_estimated_value+amount))
        self.Gen = self.request("INSERT INTO Person (pid, name, surname, exemption) VALUES (generate_series({0}, {1}), random_string  (6), random_string (9), 'disabled');".format(start_estimated_value+amount+1, start_estimated_value+2*amount))

        self.Gen = self.request("INSERT INTO stop (sid, Address) VALUES (generate_series({0}, {1}), random_string(15));".format(start_estimated_value, start_estimated_value+amount))

        self.Gen = self.request("INSERT INTO ticket (TID, Price, Operation_time) VALUES (generate_series({0},{1}), generate_series({2}, {3}), generate_series('{4}'::timestamp, '{5}','24 hours'));".format(start_estimated_value, start_estimated_value+amount, 0, 20,  str(datetime.datetime.now()), str( datetime.datetime.now() + timedelta(days=amount))))

        self.Gen = self.request("INSERT INTO Transport (Car_number, Route_number) VALUES (generate_series({0},{1}), generate_series({0}, {1}));".format(start_estimated_value, start_estimated_value+amount))

        self.Gen = self.request("INSERT INTO schedule (scheduleid, car_number, sid, time) VALUES (generate_series({0}, {1}), generate_series({0},{1}), generate_series({0}, {1}), generate_series('{2}'::timestamp, '{3}','24 hours'));".format(start_estimated_value, start_estimated_value+amount, str(datetime.datetime.now()), str( datetime.datetime.now() + timedelta(days=amount))))

        self.Gen = self.request("INSERT INTO ownership (tid, pid) VALUES (generate_series({0}, {1}), generate_series({0},{1}));".format(start_estimated_value, start_estimated_value+amount))

        self.Gen = self.request("INSERT INTO trip (tripid, car_number, tid, start_time, end_time) VALUES (generate_series({0}, {1}),generate_series({0}, {1}),generate_series({0}, {1}),generate_series('{2}'::timestamp, '{3}','10 minutes'), generate_series('{4}'::timestamp, '{5}','10 minutes'));".format(start_estimated_value,
                                                                                                                                                                                                                                                                                                         start_estimated_value+amount, str(datetime.datetime.now()), str( datetime.datetime.now() + timedelta(minutes=amount*10)),
                                                                                                                                                                                                                                                                                                         str( datetime.datetime.now() + timedelta(minutes=20)), str( datetime.datetime.now() + timedelta(minutes=20+amount*10))))
        print(start_estimated_value)

        data = {'last_number': start_last_number + amount, 'estimated_value': start_estimated_value + amount}
        with open('data.json', 'w+') as f:
            json.dump(data, f)

    def gen_values(self, Controller):
        print(Controller)
        self.generate_values()
        if self.Gen:
            Controller.gen_label.setText('Done!')
        else:
            Controller.gen_label.setText('Error while generating!')

    def requestFormat(self, comboTable, comboAction, textAction, Controller):
        Controller.gen_label.setText('')

        if comboAction == 'delete':
            Controller.Flag = self.delete_request(comboTable, textAction)
            if not Controller.Flag:
                Controller.error.setText(str(self.error))
            else:
                Controller.error.setText('Done')
        elif comboAction == 'insert':
            self.Flag = self.insert_request(comboTable, textAction)
            if not self.Flag:
                Controller.error.setText(str(self.error))
            else:
                Controller.error.setText('Done')
        elif comboAction == 'update':
            self.Flag = self.update_request(comboTable, textAction)
            if not self.Flag:
                Controller.error.setText(str(self.error))
            else:
                Controller.error.setText('Done')

    def full_string(self, Controller):
        self.columns = str()
        Controller.full_text = Controller.textSearch.toPlainText().split(' ')
        Controller.full_search_table = Controller.full_text_box.currentText()       # from which table to search
        print(Controller.full_text)
        print(Controller.full_search_table)
        if len(Controller.full_text) == 1:
            Controller.textSearch.setText('Wrong entering')
            return
        req = ''
        temp = ''
        req = "SELECT * FROM {1} WHERE {2} LIKE '{3}';".format(Controller.full_text[0], Controller.full_search_table, Controller.full_text[0], Controller.full_text[1])
        name = self.get_request(req)
        if len(Controller.full_text) == 1:
            Controller.textSearch.setText('Wrong entering')
            return
        if self.erFlag:
            Controller.textSearch.setText(str(self.gen_error))
            return
        for word in name:
            for i in word:
                temp += str(i) + ' '
            temp+= '\n'
        for word in self.colnames:
            Controller.columns += word + "          "
        Controller.columns += '\n'
        Controller.textSearch.setText(Controller.columns + temp)
