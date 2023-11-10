from threading import Thread
from gift_card import Card_Manager

def hack_boba_shop(boba_shop: Card_Manager):
    counter = 0
    for _ in range(100):
        thread_1 = Thread(target=boba_shop.transfer_points, args=(1, 2, 100))
        thread_2 = Thread(target=boba_shop.transfer_points, args=(1, 2, 100))

        thread_1.start()
        thread_2.start()

        thread_1.join()
        thread_2.join()

        if boba_shop.get_balance(1) < 0:
            print(counter)
            break
        else:
            boba_shop.transfer_points(2, 1, 100)
        counter += 1


def main():
    boba_shop = Card_Manager(5, 0)
    boba_shop.deposit(1, 100)
    boba_shop.get_all_cards()
    boba_shop.remove_card(5)
    boba_shop.get_all_cards()

    # hack_boba_shop(boba_shop)
    
    # boba_shop.get_all_cards()

if __name__ == "__main__":
    main()
