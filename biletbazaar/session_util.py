
#buy 1
kbuy_ticket_id = 'kbuy_ticket_id'
kbuy_ticket_count = 'kbuy_ticket_count'

#buy 2
kbuy_ship_name = 'kbuy_ship_name'
kbuy_ship_surname = 'kbuy_ship_surname'
kbuy_ship_city = 'kbuy_ship_city'
kbuy_ship_neighbourhood = 'kbuy_ship_neighbourhood'
kbuy_ship_address = 'kbuy_ship_address'
kbuy_ship_address2 = 'kbuy_ship_address2'

#buy 3
kbuy_cardholder_name = 'kbuy_cardholder_name'
kbuy_cardholder_surname = 'kbuy_cardholder_surname'
kbuy_card_number = 'kbuy_card_number'
kbuy_card_expiration_month = 'kbuy_card_expiration_month'
kbuy_card_expiration_year = 'kbuy_card_expiration_year'
kbuy_card_cvc2 = 'kbuy_card_cvc2'

#buy 4
kbuy_ticket_final_seat = 'kbuy_ticket_final_seat'
kbuy_ticket_seat_from = 'kbuy_ticket_seat_from'

buy1_elements = [kbuy_ticket_id,kbuy_ticket_count]
buy2_elements = [kbuy_ship_name, kbuy_ship_surname, kbuy_ship_city, kbuy_ship_neighbourhood, kbuy_ship_address, kbuy_ship_address2]
buy3_elements = [kbuy_cardholder_name, kbuy_cardholder_surname, kbuy_card_number, kbuy_card_expiration_month, kbuy_card_expiration_year, kbuy_card_cvc2]
buy4_elements = [kbuy_ticket_final_seat, kbuy_ticket_seat_from]

#sell 2
ksell_event_id = 'ksell_event_id'
ksell_ticket_count = 'ksell_ticket_count'
ksell_seat_category = 'ksell_seat_category'
ksell_seat_row = 'ksell_seat_row'
ksell_seat_number_from = 'ksell_seat_number_from'
ksell_seat_number_to = 'ksell_seat_number_to'

#sell 3
ksell_ticket_face_value = 'ksell_ticket_face_value'
ksell_ticket_sell_value = 'ksell_ticket_sell_value'

#sell 4
ksell_ship_name = 'ksell_ship_name'
ksell_ship_surname = 'ksell_ship_surname'
ksell_ship_city = 'ksell_ship_city'
ksell_ship_neighbourhood = 'ksell_ship_neighbourhood'
ksell_ship_address = 'ksell_ship_address'

sell2_elements = [ksell_event_id, ksell_ticket_count, ksell_seat_category, ksell_seat_row, ksell_seat_number_from, ksell_seat_number_to]
sell3_elements = [ksell_ticket_face_value, ksell_ticket_sell_value]
sell4_elements = [ksell_ship_name, ksell_ship_surname, ksell_ship_city, ksell_ship_neighbourhood, ksell_ship_address]

#generic
kselected_city = 'kselected_city'

class session_util(object):
    
    @staticmethod
    def clear_buy_steps4(request):
        for element in buy4_elements:
            request.session[element] = None
        
    @staticmethod
    def clear_buy_steps34(request):
        for element in buy3_elements:
            request.session[element] = None
            
        session_util.clear_buy_steps4(request)

    @staticmethod
    def clear_buy_steps234(request):
        for element in buy2_elements:
            request.session[element] = None
        
        session_util.clear_buy_steps34(request)
        
    @staticmethod
    def clear_buy_steps1234(request):
        for element in buy1_elements:
            request.session[element] = None
        
        session_util.clear_buy_steps234(request)

    @staticmethod
    def clear_sell_steps4(request):
        for element in sell4_elements:
            request.session[element] = None
        
    @staticmethod
    def clear_sell_steps34(request):
        for element in sell3_elements:
            request.session[element] = None
            
        session_util.clear_buy_steps4(request)

    @staticmethod
    def clear_sell_steps234(request):
        for element in sell2_elements:
            request.session[element] = None
        
        session_util.clear_buy_steps34(request)
        
    @staticmethod
    def clear_sell_steps1234(request):
        session_util.clear_buy_steps234(request)

    

        
        

