
import pymysql
import curses


class Connector:

    def __init__(self, database, user, password, hostname='localhost', port=3306):
        try:
            port = int(port)
            self.conn = pymysql.connect(host=hostname, port=port,
                                        user=user, passwd=password, db=database)
            self.cursor = self.conn.cursor()
        except (pymysql.err.InternalError, pymysql.err.OperationalError) as e:
            self.close(str(e))

    def close(self, err_string):
        curses.nocbreak()
        curses.echo()
        curses.curs_set(0)
        curses.endwin()
        print(err_string)
        quit(2)

    def query_exec(self, query_string):
        self.cursor.execute(query_string)
        return self.cursor.fetchall()

    def get_all_columns(self, table_name):
        self.cursor.execute('DESC ' + table_name + ';')
        cols = self.cursor.fetchall()
        return cols

    def select_all_from(self, table_name):
        self.cursor.execute('SELECT * FROM ' + table_name + ';')
        return self.cursor.fetchall()

    def show_tables(self):
        self.cursor.execute("show tables;")
        tuples = self.cursor.fetchall()
        tables = []
        for raw in tuples:
            tables.append(raw[0])
        return tables
