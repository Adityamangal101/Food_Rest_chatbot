from fastapi import FastAPI ,Request, Response
from fastapi.responses import JSONResponse
import db_helper
from genric_fun import extract_session_id , get_str_resp_from_fooddict
app=FastAPI()

# @app.middleware("http")
# async def add_ngrok_skip_header(request: Request, call_next):
#     response: Response = await call_next(request)
#     response.headers["ngrok-skip-browser-warning"] = "true"
#     return response

inprogress_order={}

@app.post("/webhook")
async def handle_request(request: Request):
    #Retriving the json data from request
    payload = await request.json()

    # Extract the neccessary info from payload
    # based on the structure of the webhookRequest from Dialogueflow
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']

    intent_handler ={
    "track.order-context: ongoing-tracking":track_order,
    "order.add- context: ongoing-order":add_order,
    "order.remove- context: ongoing-order":remove_order,
    "order.complete- context: ongoing-order":order_complete,
    "new.order":new_order
    }
    session_id=extract_session_id(output_contexts[0]['name'])

    return intent_handler[intent](parameters,session_id)

def new_order(parameters:dict,session_id:str):
    if session_id in inprogress_order:
        del inprogress_order[session_id]

def add_order(parameters:dict,session_id:str):
    food_items=parameters['food-item']  
    quantity=parameters['number']

    if len(food_items) !=len(quantity):
        fulfillment_Text =f"Sorry i didn't understand . Can you please specify food item quantity properly"
    else:
        new_food_dict=dict(zip(food_items,quantity))

        if session_id in inprogress_order:
            current_food_dict=inprogress_order[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_order[session_id]=current_food_dict
        else:
           inprogress_order[session_id]=new_food_dict

        order_str=get_str_resp_from_fooddict(inprogress_order[session_id])

        fulfillment_Text=f"So far you have {order_str}. Do you need anything else"
    

    return JSONResponse(content={
         "fulfillmentText":fulfillment_Text
    })

def order_complete(parameters:dict,session_id:str):
    if session_id not in inprogress_order:
        fulfillment_text="I am having trouble finding your order . Sorry can you order again"
    else:
        order=inprogress_order[session_id]
        order_id=save_to_db(order)

        if order_id ==-1:
            fulfillment_text="Sorry I couldn't process your order due to backend error" \
                             "Please place a new order again"
        else:
            order_total= db_helper.get_total_order_price(order_id)
            fulfillment_text=f"Awesome . We have placed your order. "\
                             f"Here is your order id #{order_id}. "\
                             f"Your order total is ${order_total} which you can pay at time of delivery!"

        del inprogress_order[session_id]

    return JSONResponse(content={
         "fulfillmentText":fulfillment_text
    })

def save_to_db(order: dict):
    # order={'pizza':2,"lassi":3}
    next_order_id=db_helper.get_next_order_id()
    
    for food_item, quantity in order.items():
        rcode=db_helper.insert_order_item(food_item,quantity,next_order_id)

        if rcode==-1:
            return -1
        
    db_helper.insert_order_tracking(next_order_id,"in progress")

    return next_order_id


def track_order(parameters:dict,session_id:str):
    order_id=int(parameters["number"])
    order_status= db_helper.get_order_status(order_id)
    
    if order_status:
        fulfillmentText=f"Your order status for order id {order_id} is {order_status}"
    else:
        fulfillmentText=f"No order found with order id {order_id}"

    return JSONResponse(content={
         "fulfillmentText":fulfillmentText
    })

def remove_order(parameters:dict,session_id:str):
    if session_id not in inprogress_order:
        fulfillment_text="Sorry you dont have any order please order first"
    else:
    
        food_items=parameters["food-item"]
        current_food_dict=inprogress_order[session_id]

        removed_items=[]
        no_such_items=[]
        fulfillment_text=[]
        for item in food_items:
            if item not in current_food_dict:
                no_such_items.append(item)
                
            else:
                 removed_items.append(item)
                 del current_food_dict[item]
        
        if len(removed_items)>0:
            fulfillment_text.append(f"Removed{','.join(removed_items)} from your order")
        if len(no_such_items)>0:
            fulfillment_text.append(f"Your current order does not have {','.join(no_such_items)}")
        if len(current_food_dict.keys())==0:
            fulfillment_text.append("Your order list is empty")
        else:
            order_str=get_str_resp_from_fooddict(current_food_dict)
            fulfillment_text.append(f"Here is what is left inyour order:{order_str}")

        inprogress_order[session_id]=current_food_dict  
        fulfillment_text = " ".join(fulfillment_text)  

    return JSONResponse(content={
       "fulfillmentText":fulfillment_text
    })
