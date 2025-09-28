"""
Payment controller
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from commands.write_payment import create_payment
from queries.read_payment import get_payment_by_id

def create_payment(order_id, user_id, total_amount):
    """Create payment, use WritePayment model"""
    try:
        return create_payment(order_id, user_id, total_amount)
    except ValueError as e:
        print(e)
        return str(e)
    except Exception as e:
        print(e)
        return "Une erreur s'est produite lors de la création de l'enregistrement. Veuillez consulter les logs pour plus d'informations."

def get_payment(payment_id):
    return get_payment_by_id(payment_id)