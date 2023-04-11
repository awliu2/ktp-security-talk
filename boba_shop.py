from threading import Thread
import json

class Card_Manager:
    def __init__(self, num_cards = 0, starting_balance = 0):
        self.cards = {}
        
        for card_id in range(1, num_cards + 1):
            self.cards[card_id] = starting_balance

        with open('cards_data', 'w') as f:
            f.write(json.dumps(self.cards))
    
    def load_cards(self):
            success = False
            while not success:
                with open('cards_data', encoding='utf-8', errors='ignore') as f:
                    try:
                        data = json.loads(f.read())
                        for k, v in data.items():
                            self.cards[int(k)] = int(v)
                        success = True
                    except Exception as e:
                        print(e)

    
    def save_cards(self):
        with open('cards_data', 'w') as f:
            f.write(json.dumps(self.cards))

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
        
        self.cards.remove(card)
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
        print('____________\n| ID | BAL |\n+----------+')
        for card in self.cards.items():
            print('| {:>2} | {:^4}|'.format(*card))
        print('+----------+')
        
boba_shop = Card_Manager(5)
boba_shop.deposit(1, 100)
boba_shop.get_all_cards()


def hack_boba_shop():
    counter = 0
    for _ in range(100):
        thread_1 = Thread(target = boba_shop.transfer_points, args=(1, 2, 100))
        thread_2 = Thread(target = boba_shop.transfer_points, args=(1, 2, 100))
        
        thread_1.start()
        thread_2.start()

        thread_1.join()
        thread_2.join()
        
        if (boba_shop.get_balance(1) == -100):
            print(counter)
            break
        else:
            boba_shop.transfer_points(2, 1, 100)
        counter += 1

# hack_boba_shop()
# boba_shop.get_all_cards()