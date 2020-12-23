class Category:

    def __init__(self, category):
        self.category = category
        self.ledger = []

    def __str__(self):
        # creating the title
        title = "*"*(int((30 - len(self.category)) / 2)) + \
            self.category + "*"*(int((30 - len(self.category)) / 2))
        title = title if len(title) == 30 else title + "*"*(30-len(title))
        # creating budget items
        bItems = ""
        for item in self.ledger:
            desc = item["description"]
            desc = desc if len(desc) < 23 else desc[:23]
            amount = str("%.2f" % item["amount"])

            bItems += desc + " "*(30 - (len(desc)+len(amount))) + amount + "\n"
        # total budget
        total = "Total: " + str(self.get_balance())

        return title + "\n" + bItems + total

    def deposit(self, amount=0.0, description=""):
        self.ledger.append({
            "amount": amount,
            "description": description
        })

    def withdraw(self, amount=0.0, description=""):
        if self.check_funds(amount):
            self.ledger.append({
                "amount": amount*-1,
                "description": description
            })
            return True
        return False

    def get_balance(self):
        balance = 0.0
        for i in self.ledger:
            balance += i["amount"]
        return balance

    def transfer(self, amount="", categorey=""):
        if self.check_funds(amount):
            self.ledger.append({
                "amount": amount*-1,
                "description": "Transfer to " + categorey
            })
            return True
        return False

    def check_funds(self, amount):
        return True if self.get_balance() > amount else False


d = Category("Food")
d.deposit(1000, "initial deposit ")
d.withdraw(10.15, "groceries")
d.withdraw(15.89, "restaurant and more food")
d.transfer(50.00, "Clothing")

d2 = Category("Transport")
d2.deposit(500, "initial deposit ")
d2.withdraw(90.15, "groceries")
d2.withdraw(12.89, "restaurant and more food")
d2.transfer(70.00, "Clothing")


def create_spend_chart(categories):

    chartData = []
    chart = ""

    for item in categories:
        deposits = 0.0
        withdraws = 0.0

        for ledgerItem in item.ledger:
            if ledgerItem["amount"] < 0:
                withdraws += abs(ledgerItem["amount"])
            else:
                deposits += ledgerItem["amount"]

        chartData.append({
            "category": item.category,
            "percentage": int((deposits - (deposits - withdraws)) / deposits * 100)
        })

    # creating the top part of the chart
    for i in reversed(range(11)):
        chart += (" "*(3-len(str(i*10))))+str(i*10)+"|"
        for data in chartData:
            if data["percentage"] > i*10:
                chart += "o "
        chart += "\n"

    return chart


print(create_spend_chart([d, d2]))
