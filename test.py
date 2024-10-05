from yoomoney import Authorize, Client, Quickpay
import requests

from setting import settings

# a = Authorize(
#     client_id="45B4A444013D5B6E9B3BEAAE2BBE990DF923CAABDD35196439FD2F79AC310CE4",
#     redirect_uri="http://t.me/help_for_problem_bot",
#     client_secret="803070098AA61E9E28C5B8F853B798A475B06D528B225E03AD44DD849EBDD9879563DECC7931C52F659D7C25E0214AECB5501B13A98E0516E525E22002C177B7",
#     scope=["account-info",
#            "operation-history",
#            "operation-details",
#            "incoming-transfers",
#            "payment-p2p",
#            "payment-shop",
#            ]
# )
# print(a)
# token = '410019405101520.8A1E57D597BD8858559B03A5F18BC7D4733B32BEA6EBA8C4ADB8891874EA14A20820DB42055668B0F5107FA835B224E74EBCD6356613386BFF0CB62B5D0103B67BD1E69E348F4646E57EEB6243E585F4F4C1CF730C29BE928E0288BD7B730EB54D3FEA275DF331A26FDD815B3F63CDB77F817E46E46BE36910DB14CB51DE93C9'
# client = Client(token)
#
# user = client.account_info()
#
# print("Account number:", user.account)
# print("Account balance:", user.balance)
# print("Account currency code in ISO 4217 format:", user.currency)
# print("Account status:", user.account_status)
# print("Account type:", user.account_type)
#
# print("Extended balance information:")
# for pair in vars(user.balance_details):
#     print("\t-->", pair, ":", vars(user.balance_details).get(pair))
#
# print("Information about linked bank cards:")
# cards = user.cards_linked
#
# if len(cards) != 0:
#     for card in cards:
#         print(card.pan_fragment, " - ", card.type)
# else:
#     print("No card is linked to the account")
quickpay = Quickpay(
            receiver="410019405101520",
            quickpay_form="shop",
            targets="Sponsor this project",
            paymentType="SBP",
            label="",
            sum=10,
            )
print(quickpay.base_url)
print(quickpay.redirected_url)

client = Client(settings['TOKEN_YOOMONEY'])
history = client.operation_history(label="VPN_сбор.")
print("List of operations:")
print("Next page starts with: ", history.next_record)
for operation in history.operations:
    print()
    print("Operation:", operation.operation_id)
    print("\tStatus     -->", operation.status)
    print("\tDatetime   -->", operation.datetime)
    print("\tTitle      -->", operation.title)
    print("\tPattern id -->", operation.pattern_id)
    print("\tDirection  -->", operation.direction)
    print("\tAmount     -->", operation.amount)
    print("\tLabel      -->", operation.label)
    print("\tType       -->", operation.type)
    print("\tDescription -->", operation.description)
