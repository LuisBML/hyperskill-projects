# Write your code here
import argparse


class Card:

    def __init__(self, user_term, user_definition, user_mistakes) -> None:
        self.term = user_term
        self.definition = user_definition
        self.mistakes = user_mistakes


class FlashCard:

    def __init__(self, imp_file, exp_file):

        self.log = ""
        self.cards = []
        self.terms = []
        self.definitions = []
        self.mistakes = [0]
        self.imp_file = imp_file
        self.exp_file = exp_file

    def update_mistakes(self):
        self.mistakes = [card.mistakes for card in self.cards]

    def update_cards(self):
        self.terms = [card.term for card in self.cards]
        self.definitions = [card.definition for card in self.cards]
        self.update_mistakes()

    def hardest_card(self):
        max_value = max(self.mistakes)
        if max_value:

            no_max_values = self.mistakes.count(max_value)
            max_index = -1
            hardest_terms = []

            for _ in range(no_max_values):
                max_index = self.mistakes.index(max_value, max_index + 1)
                hardest_terms.append(self.terms[max_index])

            if len(hardest_terms) == 1:
                text = f'The hardest card is "{hardest_terms[0]}". You have {max_value} errors answering it.\n\n'
            else:
                text = 'The hardest cards are "'
                text += '", "'.join(hardest_terms)
                text += f'". You have {max_value} errors answering them.\n\n'
        else:
            text = 'There are no cards with errors.\n\n'
        self.log += text
        print(text, end="")

    def set_term(self):
        text = "The card:\n"
        self.log += text
        print(text, end="")

        while True:
            user_term = input()
            self.log += f'{user_term}\n'
            if self.cards and user_term in self.terms:
                text = f'The term "{user_term}" already exists. Try again:\n'
                self.log += text
                print(text, end="")
            else:
                return user_term

    def set_definition(self):
        text = f"The definition of the card:\n"
        self.log += text
        print(text, end="")
        while True:
            user_def = input()
            self.log += f'{user_def}\n'
            if self.cards and user_def in self.definitions:
                text = f'The definition "{user_def}" already exists. Try again:\n'
                self.log += text
                print(text, end="")
            else:
                return user_def

    def add_card(self):
        term = self.set_term()
        definition = self.set_definition()
        self.cards.append(Card(term, definition, 0))
        self.update_cards()

        text = f'The pair ("{term}":"{definition}") has been added.\n\n'
        self.log += text
        print(text, end="")

    def remove_card(self):
        text = "Which card?\n"
        self.log += text
        print(text, end="")
        card_name = input()
        self.log += f'{card_name}\n'

        try:
            index = self.terms.index(card_name)
            self.cards.pop(index)
            self.update_cards()
            text = "The card has been removed.\n\n"
            self.log += text
            print(text, end="")
        except ValueError:
            text = f'Can\'t remove "{card_name}": there is no such card.\n\n'
            self.log += text
            print(text, end="")

    def import_file(self):
        if self.imp_file:
            file_name = self.imp_file
        else:
            text = "File name:\n"
            self.log += text
            print(text, end="")
            file_name = input()
        self.log += f'{file_name}\n'

        try:

            with open(file_name, "r") as file:
                pairs = file.read().splitlines()
                for pair in pairs:

                    f_term, f_definition, f_mistakes = pair.split()
                    if f_term in self.terms:
                        index = self.terms.index(f_term)
                        self.cards.pop(index)
                    self.cards.append(Card(f_term, f_definition, int(f_mistakes)))

                text = f"{len(pairs)} cards have been loaded.\n\n"
                self.log += text
                print(text, end="")
                self.update_cards()

        except FileNotFoundError:
            text = "File not found.\n\n"
            self.log += text
            print(text, end="")

    def export_file(self):
        if self.exp_file:
            file_name = self.exp_file
        else:
            text = "File name:\n"
            self.log += text
            print(text, end="")
            file_name = input()
        self.log += f'{file_name}\n'

        with open(file_name, "w") as file:
            for card in self.cards:
                file.write(f"{card.term} {card.definition} {card.mistakes}\n")

        text = f"{len(self.cards)} cards have been saved..\n\n"
        self.log += text
        print(text, end="")

    def log_console(self):
        text = "File name:\n"
        self.log += text
        print(text, end="")

        file_name = input()
        self.log += f'{file_name}\n'

        with open(file_name, "w") as file:
            file.write(self.log)
            text = "The log has been saved.\n\n"
            self.log += text
            print(text, end="")

    def ask(self):
        text = "How many times to ask?\n"
        self.log += text
        print(text, end="")
        num = int(input())
        self.log += f'{str(num)}\n'

        for i in range(0, num):
            card_i = i % (len(self.terms))
            term = self.terms[card_i]
            definition = self.definitions[card_i]
            card_obj = self.cards[card_i]

            text = f'Print the definition of "{term}":\n'
            self.log += text
            print(text, end="")
            answer = input()
            self.log += f'{answer}\n'

            if answer == definition:
                text = "Correct!\n\n"
                self.log += text
                print(text, end="")
            elif answer in self.definitions:
                card_obj.mistakes += 1
                term_index = self.definitions.index(answer)
                correct_term = self.terms[term_index]
                text = f'Wrong. The right answer is "{definition}", ' \
                       f'but your definition is correct for "{correct_term}".\n\n'
                self.log += text
                print(text, end="")
            else:
                card_obj.mistakes += 1
                text = f'Wrong. The right answer is "{definition}".\n\n'
                self.log += text
                print(text, end="")
        self.update_mistakes()
        print()

    def reset(self):
        for card in self.cards:
            card.mistakes = 0
        self.mistakes = [0] * len(self.cards)
        text = "Card statistics have been reset.\n\n"
        self.log += text
        print(text, end="")

    def start_menu(self):
        actions = {"add": self.add_card, "remove": self.remove_card,
                   "import": self.import_file, "export": self.export_file,
                   "ask": self.ask, "log": self.log_console,
                   "hardest card": self.hardest_card, "reset stats": self.reset}

        if self.imp_file:
            actions["import"]()

        while True:

            text_menu = "Input the action (add, remove, import, export, ask, exit, " \
                        "log, hardest card, reset stats):\n"
            self.log += text_menu
            print(text_menu, end="")

            action = input()
            self.log += f'{action}\n'
            if action == "exit":
                text_menu = "Bye bye!\n"
                self.log += text_menu
                print(text_menu, end="")
                if self.exp_file:
                    actions["export"]()
                break
            try:
                actions[action]()  # call function
            except KeyError:
                print("Not a valid option.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="When learning a new language, it can be hard to remember "
                                                 "all the new vocabulary, which is exactly where flashcards "
                                                 "can help. ")
    parser.add_argument("-imp", "--import_from", default="")
    parser.add_argument("-exp", "--export_to", default="")
    args = parser.parse_args()

    my_cards = FlashCard(args.import_from, args.export_to)
    my_cards.start_menu()
