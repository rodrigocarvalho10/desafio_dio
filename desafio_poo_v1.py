import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class Client:
    def __init__(self, address):
        self.address = address
        selfaccounts = []

    def exec_transation(self, account, transation):
        transation.register(account)

    def addaccount(self, account):
        self.account.append(account)


class NaturalPerson(Client):
    def __init__(self, name, cpf, date_birth, address):
        super().__init__(address)
        self.name = name
        self.cpf = cpf
        self.date_birth = date_birth


class Account:
    def __init__(self, number, Client):
        self._balance = 0
        self._number = number
        self._agency = "0001"
        self._Client = Client
        self._historic = Historic()

    @classmethod
    def new_account(cls, client, number):
        return cls(number, client)

    @property
    def balance(self):
        return self._balance

    @property
    def number(self):
        return self._number

    @property
    def agency(self):
        return self._agency

    @property
    def client(self):
        return self._client

    @property
    def historic(self):
        return self._historic

    def withdraw(self, value):
        balance = self.balance
        exceeded_balance = value > balance
        if exceeded_balance:
            print("Operation failed! You don't have enough balance")

        elif value > 0:
            self._balance -= value
            print(f"Withdraw of R$ {value:.2f} was successful")
            return True
        else:
            print("Operation failed! The value entered is invalid")
        return False

    def deposit(self, value):
        if value > 0:
            self._balance += value
            print(f"Deposit of R$ {value:.2f} was successful")
        else:
            print("Operation failed! The value entered is invalid")
            return False
        return True


class CheckingAccount(Account):
    def __init__(self, number, client, limit=500, limit_withdraw=3):
        super().__init__(number, client)
        self._limit = limit
        self._limit_withdraw = limit_withdraw

    def withdraw(self, value):
        balance = self.balance
        exceeded_balance = value > balance
        exceeded_limit = value > self._limit
        exceeded_withdraw = self._historic.withdraws >= self._limit_withdraw

        if exceeded_balance:
            print("Operation failed! You don't have enough balance")
        elif exceeded_limit:
            print("Operation failed! You don't have enough limit")
        elif exceeded_withdraw:
            print("Operation failed! Number of daily withdrawals exceeded")
        elif value > 0:
            self._balance -= value
            self._historic.withdraws += 1
            print(f"Withdraw of R$ {value:.2f} was successful")
            return True
        else:
            return super().withdraw(value)
        return False

    def __str__(self):
        return f"""\
            Account: {self.number}
            Agency: {self.agency}
            Client: {self.client.name}
        """


class Historic:
    def __init__(self):
        self._transations = []

    @property
    def transations(self):
        return self._transations

    def add_transation(self, transation):
        self._transations.append(
            {
                "type": transation.__class__.__name__,
                "value": transation.value,
                "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        )


class Transation(ABC):
    @property
    @abstractproperty
    def value(self):
        pass

    @abstractclassmethod
    def register(self, account):
        pass


class Withdraw(Transation):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def register(self, account):
        success_transation = account.withdraw(self.value)
        if success_transation:
            account.historic.add_transation(self)


class Deposit(Transation):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def register(self, account):
        success_transation = account.deposit(self.value)
        if success_transation:
            account.historic.add_transation(self)


def menu():
    menu = """\n
    ======= Banco RCarvalho ========

    Digite a opção desejada:

    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair

    => """
    return input(textwrap.dedent(menu))


def filter_user(cpf, clients):
    clients_filtered = [client for client in clients if client.cpf == cpf]
    return clients_filtered[0] if clients_filtered else None


def get_account_client(client):
    if not client.accounts:
        print("\nCustomer does not have a bank account")
        return
    return client.accounts[0]


def deposit(clients):
    cpf = input("Enter the CPF of the account holder: ")
    client = filter_user(cpf, clients)

    if not client:
        print("\nOperation failed! User not found")
        return
    value = float(input("Enter the deposit amount: "))
    transation = Deposit(value)

    account = get_account_client(client)
    if not account:
        print("\nOperation failed! Account not found")
        return
    client.exec_transation(account, transation)


def withdraw(clients):
    cpf = input("Enter the CPF of the account holder: ")
    client = filter_user(cpf, clients)

    if not client:
        print("\nOperation failed! User not found")
    return
    value = float(input("Enter the withdrawal amount: "))
    transation = Withdraw(value)

    account = get_account_client(client)
    if not account:
        return

    client.exec_transation(account, transation)


def view_extract(clients):
    cpf = input("Enter the CPF of the account holder: ")
    client = filter_user(cpf, clients)

    if not client:
        print("\nOperation failed! User not found")
        return
    account = get_account_client(client)
    if not account:
        return
    print("\n================ EXTRACT ================")
    transation = account.historic.transations

    extract = ""
    if not transation:
        extract = "No transactions found"
    else:
        for transation in transation:
            extract += f"""\
                Type: {transation['type']}
                Value: R$ {transation['value']:.2f}
                Date: {transation['date']}
            """
    print(textwrap.dedent(extract))
    print(f"\nBalance: R$ {account.balance:.2f}")
    print("========================================")


def create_user(clients):
    cpf = input("Enter the CPF (format: 99999999999): ")
    client = filter_user(cpf, clients)

    if client:
        print("\nOperation failed! User already registered with the informed CPF")
        return

    name = input("Full name: ")
    date_birth = input("Date of Birth (dd-mm-yyyy): ")
    address = input(
        "Address (street, number - Neighborhood - City/state of the State): ")

    clients.append(NaturalPerson(name, cpf, date_birth, address))
    print("Success: User registered successfully")


def create_account(agency, number_account, clients):
    cpf = input("Enter the user's CPF: ")
    client = filter_user(cpf, clients)

    if client:
        print("\nSuccess: account created successfully")
        return CheckingAccount(number_account, client)
    print("\nOperation failed! User not found, account could not be created")


def list_accounts(accounts):
    for account in accounts:
        print("=" * 100)
        print(textwrap.dedent(str(account)))


def main():
    clients = []
    accounts = []
    number_account = 1

    while True:
        option = menu()

        if option == "d":
            deposit(clients)

        elif option == "s":
            withdraw(clients)

        elif option == "e":
            view_extract(clients)

        elif option == "nu":
            create_user(clients)

        elif option == "nc":
            account = create_account("0001", number_account, clients)

            if account:
                accounts.append(account)
                number_account += 1

        elif option == "lc":
            list_accounts(accounts)

        elif option == "q":
            break

        else:
            print("Invalid operation, please select the desired operation again.")


main()
