import argparse
import os

from twhousedetail.houseprice import HousePriceCommunity, HousePriceSales
from twhousedetail.tw591 import Tw591Community, Tw591Sales


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('web', choices=['591', 'price'])
    parser.add_argument('command', choices=['save', 'show', 'map', 'buy'])
    parser.add_argument('--region')
    parser.add_argument('--url')
    parser.add_argument('--overwrite', action='store_true', default=False)

    args = parser.parse_args()
    community = sales = None
    if args.web == '591':
        community = Tw591Community
        sales = Tw591Sales()
    elif args.web == 'price':
        community = HousePriceCommunity
        sales = HousePriceSales()

    if args.command == 'save':
        url = args.url.replace('\\', '')
        if 'list' in url:
            community(args.region).list(url, args.overwrite)
        else:
            community(args.region).save(url)
    elif args.command == 'show':
        if args.region:
            community(args.region).show_all()
        elif args.url:
            community.show_one(args.url.replace('\\', ''))
        else:
            result = []
            for file in os.listdir():
                if os.path.isfile(file):
                    continue
                if file.startswith(community.prefix()):
                    region = file[len(community.prefix()):]
                    print(f'save region: {region}')
                    result = result + community(region).get_all()
            with open(f'{community.prefix()}.txt', 'w') as fp:
                fp.write('\n'.join(result))
            print(f'Total: {len(result)}')
            print(f'Saved to {community.prefix()}.txt')
    elif args.command == 'buy':
        if args.url:
            sales.save(args.url.replace('\\', ''))
        else:
            sales.show()

    if args.web == '591' and args.command == 'map':
        community(args.region).map()



if __name__ == '__main__':
    main()
