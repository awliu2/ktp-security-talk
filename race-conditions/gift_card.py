import json

class Card_Manager:
    def __init__(self, num_cards=0, starting_balance=0, from_file=False):
        """
        A gift card manager that keeps track of gift card balances.
        :param num_cards: the number of cards to generate
        :param starting_balance: the starting balance of each card
        :param from_file: whether to load cards from a file or generate new ones
        """
        self.cards = {}
        if from_file:
            self.load_cards()
        else:
            for card_id in range(1, num_cards + 1):
                self.cards[card_id] = starting_balance

            with open("cards_data", "w") as f:
                f.write(json.dumps(self.cards))

    def load_cards(self):
        success = False
        while not success:
            with open("cards_data", encoding="utf-8", errors="ignore") as f:
                try:
                    data = json.loads(f.read())
                    for k, v in data.items():
                        self.cards[int(k)] = int(v)
                    success = True
                except Exception as e:
                    print(e)

    def save_cards(self):
        with open("cards_data", "w") as f:
            f.write(json.dumps(self.cards))
            f.flush()

    def add_card(self, card_id, balance):
        self.load_cards()
        if card_id in self.cards:
            return False

        self.cards[card_id] = balance
        self.save_cards()
        return True

    def remove_card(self, card):
        self.load_cards()
        if card not in self.cards:
            return False

        del self.cards[card]
        self.save_cards()
        return True

    def transfer_points(self, src, dst, amount):
        self.load_cards()
        if src not in self.cards or dst not in self.cards:
            return False

        src_balance = self.get_balance(src)

        if src_balance < amount:
            return False

        self.deduct(src, amount)
        self.deposit(dst, amount)
        return True

    def get_balance(self, card_id):
        if card_id not in self.cards:
            return False

        return self.cards[card_id]

    def deposit(self, card_id, amount):
        self.load_cards()
        if card_id not in self.cards:
            return False

        self.cards[card_id] += amount
        self.save_cards()
        return True

    def deduct(self, card_id, amount):
        self.load_cards()
        if card_id not in self.cards:
            return False

        self.cards[card_id] -= amount
        self.save_cards()
        return True

    def get_all_cards(self):
        self.load_cards()
        print("____________\n| ID | BAL |\n+----------+")
        for card in self.cards.items():
            print("| {:>2} | {:^4}|".format(*card))
        print("+----------+")
