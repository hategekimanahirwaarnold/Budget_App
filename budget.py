import math
import re 

class Category:
    def __init__(self, category):
        self.category = category
        self.ledger = []
        self.amount = 0

    def deposit(self, amount, description = ""):
        self.amount += amount
        self.ledger.append({"amount": amount, "description": description})
    
    def withdraw(self, amount, description = ""):
        if self.check_funds(amount):
            self.amount -= amount
            self.ledger.append({"amount": -amount, "description": description})
            return True
        else:
            return False

    def get_balance(self):
        return self.amount
    
    def transfer(self, amount, otherCategory):
        if self.check_funds(amount):
            self.amount -= amount
            self.ledger.append({
                "amount": -amount, 
                "description": f"Transfer to {otherCategory.category}"
            })
            otherCategory.deposit(amount, f"Transfer from {self.category}")
            return True
        else: 
            return False
            

    def check_funds(self, amount):
        if amount > self.amount:
            return False
        else:
            return True

    def __str__(self):
        string = self.category
        asterics = 30 - len(string)
        for star in range(asterics):
            if star % 2 == 0:
                string += "*"
            else:
                string = "*" + string
        string += "\n"
        # print("title: ", string)
        for item in self.ledger:
            # print("item: ", item)
            toAdd = item["description"][:23]
            # print("initial length of descrpt", len(toAdd))
            blankSpace = 23 - len(toAdd)
            # print("amount of blank space: ", blankSpace)
            for space in range(blankSpace):
                toAdd += " "
            # print("final length ofter white space: ", len(toAdd))
            decimal = item["amount"]
            formatted = f"{decimal:.2f}"
            # print("original number: ", formatted)
            decimal = formatted[:7]
            otherSpace = 7 - len(decimal)
            for space in range(otherSpace):
                toAdd += " "
            toAdd += decimal
            # print("length of to be added on string: ", len(toAdd))
            toAdd += "\n"
            string += toAdd

        current = self.amount
        # formatted = f"{current:.2f}"
        string += ("Total: " + str(current))
        return string


def create_spend_chart(categories):
    string = "Percentage spent by category\n"
    cate = []
    for categ in categories:
        toAdd = [categ.category, 0]
        for withdraw in categ.ledger:
            if withdraw["amount"] < 0:
                toAdd[1] -= withdraw["amount"]
        cate.append(toAdd)
    sum = 0
    # find the sum of all items
    for item in cate:
        sum += item[1]
    # calculate percentage of each item
    for ele in cate:
        item = math.floor(((ele[1] / sum) * 100) / 10)
        ele[1] = item * 10
    # create a chart that shows percentage of each category
    percent = 10
    while percent >= 0:
        percentage = percent * 10
        full = str(percentage)
        space1 = ""
        for space in range(3 - len(full)):
            space1 += " "
        full = space1 + full + "|" + " "
        for ele in cate:
            number = ele[1]
            if number >= percentage:
                full += "o  "
            else: 
                full += "   "
        full += ("\n")
        string += full
        percent -= 1
    string += "    -"
    splitted = []
    # get length of each category
    length = []
    for item in cate:
        string += "---"
        letters = re.findall(r"\w", item[0])
        splitted.append(letters)
        length.append(len(item[0]))
    string += "\n"
    
    maxLenght = max(length)
    increase = 0
    while increase < maxLenght:
        string += "     "
        for item in splitted:
            try:
                string += (item[int(f"{increase}")] + "  ")
            except:
                string += "   "
        if increase == maxLenght - 1:
            break
        else:
            string += "\n"

        increase += 1
    return string