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
            try:
                self.ledger.append({
                    "amount": amount*-1,
                    "description": "Transfer to " + categorey.category
                })
                categorey.ledger.append({
                    "amount": amount,
                    "description": "Transfer from " + self.category
                })
                return True
            except:
                return False
        return False

    def check_funds(self, amount):
        return True if self.get_balance() >= amount else False


def create_spend_chart(categories):

    chartData = []
    categoryNames = ""
    chart = ""
    maxCatLength = 0
    TotalWithdraws = 0.0

    # total withdraws of all the categories
    for item in categories:
        for ledgerItem in item.ledger:
            if ledgerItem["amount"] < 0:
                TotalWithdraws += abs(ledgerItem["amount"])
            maxCatLength = len(item.category) if len(
                item.category) > maxCatLength else maxCatLength

    for item in categories:
        withdraws = 0.0
        for ledgerItem in item.ledger:
            if ledgerItem["amount"] < 0:
                withdraws += abs(ledgerItem["amount"])

        maxCatLength = len(item.category) if len(
            item.category) > maxCatLength else maxCatLength

        chartData.append({
            "category": item.category,
            "percentage": int((TotalWithdraws - (TotalWithdraws - withdraws)) / TotalWithdraws * 100)
        })

    f = open("test.txt", "a")
    f.write(str(chartData))
    f.close()

    # creating the top part of the chart
    for i in reversed(range(11)):
        chart += "\n" + (" "*(3-len(str(i*10))))+str(i*10)+"| "
        for data in chartData:
            if data["percentage"] >= i*10:
                chart += "o  "
            else:
                chart += "   "

    dotLine = "\n" + " "*4 + "-"*(len(chartData)*3+1)

    # adding category names to the chart
    for i in range(maxCatLength):
        categoryNames += "\n" + " "*5
        for data in chartData:
            try:
                categoryNames += list(data["category"])[i] + "  "
            except:
                categoryNames += " "*3

    return "Percentage spent by category" + chart + dotLine + categoryNames
