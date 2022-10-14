class CSV_Modified:
    sep_char:str = ',;#!'
    def __init__(self, filename:str):
        self._filename:str = filename
    def read_table(self):
        try:
            with open(self._filename,'r') as f:
                raw_table = f.read()
        except FileNotFoundError:
            with open(self._filename,'w') as f:f.write('')
            with open(self._filename,'r') as f:
                raw_table = f.read()
        rows = [_.strip() for _ in raw_table.split(';\n;')]
        table = [row.split(self.sep_char) for row in rows]
        return table
    def write_table(self,new_table):
        rows = [self.sep_char.join(row) for row in new_table]
        raw_table = ';\n;'.join(rows)
        with open(self._filename,'w') as f:f.write(raw_table)