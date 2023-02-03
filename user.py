import pandas as pd

class UserInfo():
    def __init__(self):
        self.DB = self.set_DB()

    def set_DB(self):
        try:
            self.DB = pd.read_csv('db.csv', low_memory=False)
        except:
            self.DB = pd.DataFrame(columns=['name', 'email', 'random_code', 'permission'])
            self.DB.to_csv('db.csv')

        return self.DB

    def join(self, name):
        temp = pd.DataFrame({'name': [name], 'email': [''], 'random_code': [''], 'permission': ['guest']})
        self.DB = pd.concat([self.DB, temp])
        print(f'{name} join')

    def set_info(self, name, data_type, data_content):
        self.DB.loc[self.DB['name'] == name, data_type] = data_content

    def get_info(self, name, data_type):
        length = len(self.DB.loc[self.DB['name'] == name, data_type].values)
        if length == 0:
            return ''
        else:
            return self.DB.loc[self.DB['name'] == name, data_type].values[0]