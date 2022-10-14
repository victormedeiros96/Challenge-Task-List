from task_manager.csv_modified import CSV_Modified
import datetime,tabulate
class Task_Manager:
    _filename = 'data.csv'
    headers = ["id","description","age","priority","status"]
    def __init__(self):
        self.restore_data()
    def restore_data(self):
        def convert_str_to_date(string):
            return datetime.datetime.strptime(string,"%d/%m/%Y, %H:%M:%S")
        def adjust(row):
            row[2] = convert_str_to_date(row[2])
            return row
        csv = CSV_Modified(self._filename)
        self.table = csv.read_table()
        if len(self.table[0])==1:
            self.table[0] = len(self.headers)*['']
        else:
            self.table = list(map(adjust,self.table))
    def save_data(self):
        csv = CSV_Modified(self._filename)
        # convert the datetime to string
        def convert_date_to_str(timestamp):
            return timestamp.strftime("%d/%m/%Y, %H:%M:%S")
        def adjust(row):
            row[2] = convert_date_to_str(row[2])
            return row
        _tmp_table = [_.copy() for _ in self.table]
        try:
            _tmp_table = list(map(adjust,_tmp_table))
        except Exception as e:
            print(e)
        csv.write_table(_tmp_table)
    def add_task(self,description,priority='low'):
        last_id = self.table[-1][0]
        if last_id.isnumeric():
            id = str(int(last_id)+1)
        else:
            id = '0'
            self.table.clear()
        self.table.append([id,description,datetime.datetime.now(),priority,'pending'])
    def complete_task(self,index):
        row = [_ for _ in self.table if _[0]==str(index)][0]
        i = self.table.index(row)
        row[-1] = 'done'
        self.table[i] = row
    def list_concluded(self):
        _tmp_table = [_.copy() for _ in self.table if _[-1]=='done']
        return self.list(_tmp_table)
    def list_pending(self,raw=None):
        _tmp_table = [_.copy() for _ in self.table if _[-1]=='pending']
        if raw:
            return _tmp_table
        return self.list(_tmp_table)
    def list(self,table):
        _tmp_table = [_.copy() for _ in table]
        now = datetime.datetime.now()
        def convert_timestamp_to_delta(first_datetime):
            return now-first_datetime
        def adjust_convertion(row):
            temp = convert_timestamp_to_delta(row[2])
            if temp.days:
                row[2] = f'{temp.days} day'
            else:
                if temp.seconds>360:
                    row[2] = f'{temp.seconds//360} hour'
                elif temp.seconds>60:
                    row[2] = f'{temp.seconds//60} minute'
                else:
                    row[2] = f'{temp.seconds} second'
            return row
        try:
            _tmp_table = list(map(adjust_convertion,_tmp_table))
        except Exception as e:
            print(e)
        return tabulate.tabulate(_tmp_table, self.headers, tablefmt="fancy_grid")
    def __str__(self) -> str:
        return self.list(self.table)