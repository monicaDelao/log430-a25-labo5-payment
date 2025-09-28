"""
Payment view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import json
import numbers
import requests
from commands.write_payment import create_payment, update_status_to_paid
from views.template_view import get_param, get_template
from controllers.payment_controller import get_payment

def show_payment_form(id):
    """ Show payment form and list """
    print("payment_id", id)
    payment = get_payment(id)
    return get_template(f"""
        <h2>Paiement n° {payment['id']}</h2>
        <p>Ce paiement concerne la commande n° {payment['order_id']} de l'utilisateur n° {payment['user_id']}. Le montant à payer est de ${payment['total_amount']}.</p> 
        <p>Veuillez indiquer ci-dessous les informations relatives à votre carte de crédit afin d'effectuer le paiement.</p>
        <form method="POST" action="/payments/pay/{payment['id']}">
            <div class="mb-3">
                <label class="form-label">Numéro de Carte Crédit</label>
                <input class="form-control" type="text" name="card_number" maxlength="16" value="9999999999999999" required>
            </div>
            <div class="mb-3">
                <label class="form-label">Code CVV</label>
                <input class="form-control" type="number" name="card_code" maxlength="3" value="123" required>
            </div>
            <div class="mb-3">
                <label class="form-label">Date d'expiration</label>
                <input class="form-control" type="date" name="expiration-date" value="2038-01-19" required>
            </div>
            <p> <b>ATTENTION</b> : <span style='color:red'>Ceci n'est pas une vraie plateforme de paiement, aucune de vos informations ne sera enregistrée.</span></p>
            <button type="submit" class="btn btn-primary">Enregistrer</button>
        </form>
    """)

def add_payment(params):
    """ Add payment based on given params """
    if len(params.keys()):
        order_id = get_param(params, "order-id")
        user_id = get_param(params, "user-id")
        total_amount = get_param(params, "amount")
        result = create_payment(order_id, user_id, total_amount)
    else: 
        return f"""
            <error>
                <message>La requête est vide</message>  
            </error>
        """

    if isinstance(result, numbers.Number):
        return f"""
                <success>
                    <payment-id>{result}</payment-id>  
                </success>
            """
    else:
        return f"""
                <error>
                    <message>{result}</message>  
                </error>
            """
    
def pay(payment_id):
    """ Remove payment with given ID """
    print("start to pay")
    update_result = update_status_to_paid(payment_id)
    print("update_result", update_result)
    payload_to_store_manager = {
        "order_id": update_result["order_id"],
        "is_paid": True
    }
    response = requests.put(
        'http://store_manager:5000/orders',
        data=json.dumps(payload_to_store_manager),
        headers={'Content-Type': 'application/json'}
    )
    print(response, response.status_code)
    return  get_template(f"""
                <h2>OK</h2>
                <p>La commande {update_result["order_id"]} a été payé.</p>
            """)
    