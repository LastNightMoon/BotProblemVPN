from yoomoney import Quickpay

from database import User
from setting import settings


def get_link_for_payment(user: User):
    return Quickpay(
        receiver=f"{settings["ID_YOOMONEY"]}",
        quickpay_form="shop",
        targets="Sponsor this project",
        paymentType="SBP",
        label=f"{user.chat_id}",
        sum=2,
    ).redirected_url
