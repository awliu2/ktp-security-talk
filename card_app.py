from gift_card import Card_Manager
import sys
def main():
	from_file = False
	num_cards = 0
	starting_balance = 0
	if '-f' in sys.argv:
		from_file = True
	if '-n' in sys.argv:
		num_cards = int(sys.argv[sys.argv.index('-n') + 1])
	if '-b' in sys.argv:
		starting_balance = int(sys.argv[sys.argv.index('-b') + 1])
	
	manager = Card_Manager(num_cards, starting_balance, from_file)
	while True:
		text = input("Enter a command: ")
		parsed = text.split()
		if len(parsed) == 0:
			continue
			
		if parsed[0] == 'help':
			print('* add <card_id> <balance> - add a new card with the given balance')
			print('* delete <card_id> - delete the card with the given id')
			print('* deposit <card_id> <amount> - deposit the given amount to the card')
			print('* show - show all cards')
			print('* transfer <src> <dst> <amount> - transfer the given amount from the src card to the dst card')
			print('* deduct <card_id> <amount> - deduct the given amount from the card')
			print('* balance <card_id> - show the balance of the card')
			print('* exit - exit the program')
		
		elif parsed[0] == 'add':
			if len(parsed) != 3:
				print('Invalid format for add')
				continue
			card_id = int(parsed[1])
			balance = int(parsed[2])
			if manager.add_card(card_id, balance):
				print('Card added.')
			else:
				print('Card already exists.')

		elif parsed[0] == 'delete':
			if len(parsed) != 2:
				print('Invalid format for delete')
				continue
			card_id = int(parsed[1])
			if manager.remove_card(card_id):
				print('Card deleted.')
			else:
				print('Card does not exist.')
		
		elif parsed[0] == 'deposit':
			if len(parsed) != 3:
				print('Invalid format for deposit')
				continue
			card_id = int(parsed[1])
			amount = int(parsed[2])
			if manager.deposit(card_id, amount):
				print('Deposit successful.')
			else:
				print('Deposit failed.')
		
		elif parsed[0] == 'show':
			if len(parsed) == 1:
				manager.get_all_cards()
			if len(parsed) == 2:
				card_id = int(parsed[1])
				if manager.get_balance(card_id):
					print(f'Balance of card {card_id} is {manager.get_balance(card_id)}')
		
		elif parsed[0] == 'transfer':
			if len(parsed) != 4:
				print('Invalid format for transfer')
				continue
			src = int(parsed[1])
			dst = int(parsed[2])
			amount = int(parsed[3])
			if manager.transfer_points(src, dst, amount):
				print('Transfer successful.')
			else:
				print('Transfer failed.')
		
		elif parsed[0] == 'deduct':
			if len(parsed) != 3:
				print('Invalid format for deduct')
				continue
			card_id = int(parsed[1])
			amount = int(parsed[2])
			if manager.deduct(card_id, amount):
				print('Deduct successful.')
			else:
				print('Deduct failed.')
		
		elif parsed[0] == 'balance':
			if len(parsed) != 2:
				print('Invalid format for balance')
				continue
			card_id = int(parsed[1])
			if manager.get_balance(card_id):
				print(f'Balance of card {card_id} is {manager.get_balance(card_id)}')

		elif parsed[0] == 'exit':
			break
			
		else:
			print('Invalid command. Try help to see the list of commands.')
		

if __name__ == '__main__':
    main()