# This is where the pure backend functionality will go
class Budget:
    def __init__(self):
        self.income_dic = {
            # name: (value, method, frequency, category, description)
        }
        self.expense_dic = {}

        self.net_income = 0

    def add_income(self, name: str, date: str, value: int, method: str, frequency: str, category: str, description: str):
        self.income_dic[name] = {'value': value, 'method': method, 'frequency': frequency, 'category': category, 'description': description}
        self.net_income+=value

    def add_expense(self, name: str, date: str, value: int, method: str, frequency: str, category: str, description: str):
        self.expense_dic[name] = {'value': value, 'method': method, 'frequency': frequency, 'category': category, 'description': description}
        self.net_income-=value

    def display_income(self):
        return self.net_income

    def get_expenses(self, dic: dict):
        index = 0
        for key in dic.keys():
            title = list(dic.keys())[index]
            for key, value in dic[title].items():
                pass





