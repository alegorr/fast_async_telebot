from .models import Service, User, Transaction
from .schema import ServiceSchema, UserSchema, TransactionSchema

async def services_list():
    try:
        services_lst = await Service.get_all()
        services = list()
        for s in services_lst:
            services.append(ServiceSchema(**s))
        print(services)
        return services
    except Exception as err:
        print(err)
        return list()

async def users_list():
    try:
        users_lst = await User.get_all()
        users = list()
        for u in users_lst:
            users.append(UserSchema(**u))
        print(users)
        return users
    except Exception as err:
        print(err)
        return list()

async def transactions_list():
    try:
        transactions_lst = await Transaction.get_all()
        transactions = list()
        for t in transactions_lst:
            transactions.append(TransactionSchema(**t))
        print(transactions)
        return transactions
    except Exception as err:
        print(err)
        return list()
