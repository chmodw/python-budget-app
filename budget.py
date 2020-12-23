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

    for item in categories:
        deposits = 0.0
        withdraws = 0.0

        for ledgerItem in item.ledger:
            if ledgerItem["amount"] < 0:
                withdraws += abs(ledgerItem["amount"])
            else:
                deposits += ledgerItem["amount"]

        maxCatLength = len(item.category) if len(
            item.category) > maxCatLength else maxCatLength

        chartData.append({
            "category": item.category,
            "percentage": int((deposits - (deposits - withdraws)) / deposits * 100)
        })

    # creating the top part of the chart
    for i in reversed(range(11)):
        chart += "\n" + (" "*(3-len(str(i*10))))+str(i*10)+"| "
        for data in chartData:
            if data["percentage"] > i*10:
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

# # print("Percentage spent by category\n100|          \n 90|          \n 80|          \n 70|    o     \n 60|    o     \n 50|    o     \n 40|    o     \n 30|    o     \n 20|    o  o  \n 10|    o  o  \n  0| o  o  o  \n    ----------\n     B  F  E  \n     u  o  n  \n     s  o  t  \n     i  d  e  \n     n     r  \n     e     t  \n     s     a  \n     s     i  \n           n  \n           m  \n           e  \n           n  \n           t  ")


# print("done")
food = Category("Food")
entertainment = Category("Entertainment")
business = Category("Business")

food.deposit(900, "deposit")
entertainment.deposit(900, "deposit")
business.deposit(900, "deposit")
food.withdraw(105.55)
entertainment.withdraw(33.40)
business.withdraw(10.99)

print(create_spend_chart([business, food, entertainment]))


# Problem is with percentage calculation

# fix it and do the job assignment


# f = open("s.txt", "w+")
# f.write(create_spend_chart([business, food, entertainment]))
# f.close()
