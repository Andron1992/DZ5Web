import argparse
import asyncio
from datetime import datetime, timedelta
from privat_app import PrivatBankAPI
from utils import handle_errors


def parse_arguments():
    parser = argparse.ArgumentParser(description="Отримання курсу валют ПриватБанку за останні кілька днів.")
    parser.add_argument("days", type=int, help="кількість днів для отримання курсу валют (не більше 10)")
    args = parser.parse_args()

    if not (1 <= args.days <= 10):
        parser.error("Кількість днів повинна бути від 1 до 10")

    return args.days


async def main():
    days = parse_arguments()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    privat_app = PrivatBankAPI()

    tasks = []
    for i in range(days):
        date = (start_date + timedelta(days=i)).strftime("%d.%m.%Y")
        tasks.append(privat_app.get_exchange_rates(date))

    results = await asyncio.gather(*tasks)
    for result in results:
        if result:
            print(result)


if __name__ == '__main__':
    asyncio.run(main())
