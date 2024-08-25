from django.shortcuts import render,redirect
from cryptography.fernet import Fernet
from django.conf import settings
import os
from .models import *
from django.http import HttpResponse,JsonResponse
from datetime import date,datetime,timedelta
from django.utils import timezone

from django.db import connection
from json import dumps

import re,ast

# for which page to indicate
# login=1
# register=2
# home=3
# item detail=4
# item list=5
# item upload=6
# liveauction=7
# profile=8
# editinfo=9
#solditemdetail=10
# bought itemdetail=11
# deleteitempage=12


page_state_variable=0

item_category=['Shoes','Cars','Watches','Bikes','Cycles','Furnitures','Books','Antiques','Phones','Instruments','Clothes','Others']

def Bidbay_login(request):
     global page_state_variable
     page_state_variable=1  
     data=request.session.get('login_data')
     return render(request, 'Bidbay1/loginpage.html',data)

def Bidbay_register(request):
     global page_state_variable
     page_state_variable=2
     data=request.session.get('prevent_event_action')
     # Room.objects.all().delete()
     # reset_user_id_sequence()
     return render(request, 'Bidbay1/Registerpage.html',{"data":data})

def Bidbay_editprofileinfo(request):
     global page_state_variable
     page_state_variable=9
     user_info=get_details_for_edit_profile_info(request)
     user_profile={'user_profile_pic':get_user_profile_pic(request)[0],
                       'user_profile_pic_to_profilepage': get_user_profile_pic(request)[1],
                       'user_info':user_info}

     return render(request, 'Bidbay1/editprofileinfopage.html',user_profile)
 
def Bidbay_home(request):
     global page_state_variable,item_category
     
     page_state_variable=3
     item_newdeals_details_list = get_newdeals_item_details_in_homepage()
     items_endingsoon_details_list = get_endingsoon_item_details_in_homepage()
     live_auction_item_countdown = countdown_timer(request)
     items_livebid_details_list=get_livebid_item_details_in_homepage()     
     combined_livebid_details_list=[list(t) for t in zip(live_auction_item_countdown,items_livebid_details_list)]
     data = {
          
        'user_profile_pic': get_user_profile_pic(request)[0],
        'user_profile_pic_to_profilepage': get_user_profile_pic(request)[1],
        'newdeals_item_details': item_newdeals_details_list,
        'endingsoon_item_details':items_endingsoon_details_list,
        'item_category': item_category,
        'livebid_details':combined_livebid_details_list,
        'userindicator':request.session.get('userindicator'),

     }
 
     return render(request, 'Bidbay1/Homepage.html',data)
     

def Bidbay_uploaditem(request):
     global page_state_variable
     page_state_variable=6
     user_profile_pic={'user_profile_pic':get_user_profile_pic(request)[0],
                       'user_profile_pic_to_profilepage': get_user_profile_pic(request)[1]}
     return render(request, 'Bidbay1/uploaditempage.html',user_profile_pic)

def Bidbay_deleteitems(request):
     global page_state_variable
     page_state_variable=12
     return render(request,"Bidbay1/deleteitemspage.html",{'user_profile_pic': get_user_profile_pic(request)[0],
        'user_profile_pic_to_profilepage': get_user_profile_pic(request)[1],
        'item_details':get_item_detail_for_deleting(request),
        })
     
def Bidbay_itemdetails(request):
     global page_state_variable
     page_state_variable=4
     # data = get_item_details(request)
     
     data=None
     
     try:
          data = place_bid(request)
     except:
          data = get_item_details(request)

     
     return render(request, 'Bidbay1/itemdetailspage.html',{'data':data,
                                                  'user_profile_pic':get_user_profile_pic(request)[0],
                                                  'user_profile_pic_to_profilepage': get_user_profile_pic(request)[1],
                                                  })

def Bidbay_solditemdetail(request):
     global page_state_variable
     page_state_variable=10
     sold_item_detail=get_detail_for_sold_item(request)  
     return render(request, 'Bidbay1/solditemdetailpage.html',{'user_profile_pic':get_user_profile_pic(request)[0],
                                                               'user_profile_pic_to_profilepage': get_user_profile_pic(request)[1],
                                                               'sold_item_detail':sold_item_detail})

def Bidbay_boughtitemdetail(request):
     global page_state_variable
     page_state_variable=11
     bought_item_detail=get_detail_for_bought_item(request)
     return render(request, 'Bidbay1/boughtitemdetailpage.html',{'user_profile_pic':get_user_profile_pic(request)[0],
                                                               'user_profile_pic_to_profilepage': get_user_profile_pic(request)[1],
                                                               'bought_item_detail':bought_item_detail
                                                               })

        

def Bidbay_itemlist(request):
     
     global page_state_variable
     page_state_variable=5,
     
     
     data2 = request.session.get('data2') if request.session.get('use_data2') else None
     search_data = request.session.get('search_data') if not request.session.get('use_data2') else None
     filter_data = request.session.get('filter_data') if request.session.get("filter_search") else None
 
     if filter_data:
          if data2:
               data2['data2']=filter_data
          if search_data:
               search_data['search_data']=filter_data

     data = {
        'user_profile_pic': get_user_profile_pic(request)[0],
        'item_category': item_category,
        'itemslist': data2,
        'search_data':search_data,
        'user_profile_pic_to_profilepage': get_user_profile_pic(request)[1],
        "userindicator":request.session.get('userindicator'),
     }

     request.session['filter_search'] = False
     # request.session['use_data2'] = False
     
     return render(request,'Bidbay1/itemlistpage.html',data)

# def Bidbay_liveauction(request,room_name="good_room",user_name="good_user"):

def Bidbay_liveauction(request,room_name='',user_name=''):
     global page_state_variable
     page_state_variable=7
     live_item_detail=get_liveitem_detail(request)
     item_id=live_item_detail['data1'][2][2]
     messages_list=get_messages_for_liveauctionpage(item_id)
     print(messages_list)
     data={'user_profile_pic':get_user_profile_pic(request)[0],
           'liveauction_item_details':live_item_detail,
           'user_profile_pic_to_profilepage': get_user_profile_pic(request)[1],
           'messages':messages_list,
           'user':request.session.get('userindicator'),
          }
     return render(request, 'Bidbay1/liveauctionpage.html',data)

def Bidbay_profile(request):
     global page_state_variable
     
     page_state_variable=8
     
     data = {
        'user_profile_pic': get_user_profile_pic(request)[0],
        'user_profile_pic_to_profilepage': get_user_profile_pic(request)[1],
        'item_details':get_item_and_user_details_for_profilepage(request),
        'userindiactor':request.session.get('userindicator'),
        }
     
    
     return render(request, 'Bidbay1/profilepage.html',data)

def logout_functionality(request):
     if request.method =="POST":
          request.session['userindicator'] = ""
          return redirect("Bidbay1:Bidbay_login")

def get_messages_for_liveauctionpage(item_id):
     global page_state_variable
     item = Items.objects.get(item_id=item_id)
     room = Room.objects.get(room_name=item)
     print(item,room)
     messages=list(Message.objects.filter(room_name=room))
     messages_list=[]
     for message in messages:
          messages_list.append(message)
     return [messages_list]

def login_user_authentication(request):
     
     username=request.POST.get("username")
     password=request.POST.get("password")
     request.session["userindicator"] = username
     username_list=list(Userdetails.objects.values_list('user_name',flat=True))
     check_username = username in username_list
     request.session["login_data"]={'arg1':'0'}
     if not check_username:
          request.session["login_data"]={'arg1':'2'}
          return redirect('Bidbay1:Bidbay_login')
     
     elif match_entered_pw_with_pw_in_db(request, username,password):
          request.session["login_data"]={'arg1':'0'}
          return redirect("Bidbay1:Bidbay_home")
     else:
          request.session["login_data"]={'arg1':'1'}
          return redirect("Bidbay1:Bidbay_login")

def delete_profile(request):
     if request.method=="POST":
          user=Userdetails.objects.get(user_name=request.session.get("userindicator"))
          user.delete()
          return redirect("Bidbay1:Bidbay_login")

def search_functionality(request): 
     
     items_list=Items.objects.all()
     
     valid_items_list=[]
     
     for item in items_list:
          
          if item.item_expiry_date > timezone.now():
               valid_items_list.append(item)
          else:
               continue
          
     item_name_list=[item.item_name for item in valid_items_list ]
     
     item_category_list=[item.item_category for item in valid_items_list ]
     
     name_dict = {f"name_{index}":item_name for index,item_name in enumerate(item_name_list)}
     
     category_dict = {f"category_{index1}":item_category for index1,item_category in enumerate(item_category_list)}
     
     items_dictionary = [{f"name_{index}": name_dict[f"name_{index}"], f"category_{index}": category_dict[f"category_{index}"]}
                    for index in range(len(item_name_list))]
     
     print(items_dictionary)
     
     search_text = request.POST.get("search_box")
     
     results_dict=search_items(items_dictionary,search_text)
     
     results_list=[]
     
     for element in results_dict:
          item=list(element.items())
          results_list.append(item)
     
     item_details_set=set()
     
     for items in results_list: 
         item_detail = Items.objects.filter(item_name=items[0][1],item_category=items[1][1])
         for detail in item_detail:
               if(detail.item_expiry_date > timezone.now()):
                    item_details_set.add(detail)
     
     item_details_list=[]
     
     for detail in item_details_set:
          item_detail=[]
          item_detail.append(detail.item_id)
          item_detail.append(detail.item_name)
          item_detail.append(detail.item_description)
          item_detail.append(detail.item_final_price)
          item_detail.append((detail.item_expiry_date-timezone.now()).days)
          image_object_list=list(Images.objects.filter(item_id=detail.item_id))
          for obj in image_object_list:
               item_detail.append(obj.image_file.url)
               break
          item_detail.append(int((((detail.item_expiry_date-timezone.now()).total_seconds()) // 3600)%24))
          item_detail.append(detail.item_auction_type)
          item_details_list.append(item_detail)
     
     for item in item_details_list:
          if item[7] == 'live':
               item_detail=Items.objects.get(item_id=item[0])
               time_remaining = item_detail.item_expiry_date - timezone.now()  # Calculate time remaining
               hours = time_remaining.seconds // 3600
               minutes = (time_remaining.seconds % 3600) // 60
               seconds = time_remaining.seconds % 60
               data =[hours , minutes , seconds]
               item.append(data)
     
     request.session['search_data'] ={'search_data':item_details_list,'search_text':search_text}
     
     request.session['use_data2'] = False
     
     return redirect("Bidbay1:Bidbay_itemlist")
          
          
             

def search_items(items_dict, search_input):
    # Preprocess search input
    search_input = clean_text(search_input)
    search_tokens = search_input.split()

    # Filter by item name
    name_results = []
    for index,item in enumerate(items_dict):
        item_name = clean_text(item[f"name_{index}"])
        item_tokens = item_name.split()

        # Check if search tokens are in item tokens
        if all(token in item_tokens for token in search_tokens):
            name_results.append((item, "exact"))
        elif any(token in item_tokens for token in search_tokens):
            name_results.append((item, "partial"))

    # If there are name results, sort by relevance and return
    if name_results:
        name_results.sort(key=lambda x: 0 if x[1] == "exact" else 1)
        return [item for item, match_type in name_results]
    
    # If no name results, filter by category
    category_results = []
    for index2,item in enumerate(items_dict):
          item_category = clean_text(item[f"category_{index2}"])
          if (search_input in item_category[:-1].lower()) or (search_input in item_category.lower()):
               category_results.append(item)
          
    return category_results


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text  
    
def filtering_functionality(request):
     filter_data = request.POST.get("filter_data")
     filter_data = f"{filter_data}"
     filter_data_list = ast.literal_eval(filter_data)
     starting_price=request.POST.get('starting_price')
     name_price = request.POST.get('sort_name_price')
     auction_type = request.POST.get('sort_auction_type')
     ending_price=request.POST.get('ending_price')

     if starting_price=="": #form ma empty halda empty aayo tei bhayera none haleko
          starting_price = None
     
     if ending_price=="": #form ma empty halda empty aayo tei bhayera none haleko
          ending_price = None
     filtered_products=filter_data_list
     
     if starting_price:
            filtered_products = [product for product in filtered_products if float(product[3]) >= float(starting_price)]
     if ending_price:
            filtered_products = [product for product in filtered_products if float(product[3]) <= float(ending_price)]
     if name_price == "Name":
          filtered_products = sorted(filtered_products, key=lambda x: x[1])
     if name_price == "Price":
          filtered_products = sorted(filtered_products, key=lambda x: x[3])
     if auction_type=="Normal":
          filtered_products = [product for product in filtered_products if product[7] =="Normal"]
     if auction_type == "Live":
          filtered_products = [product for product in filtered_products if product[7] =="live"]

     request.session['filter_search'] = True
     
     request.session["filter_data"] = filtered_products
     
     return redirect("Bidbay1:Bidbay_itemlist")       
        
def save_changes_to_profile_details(request):
     
     if request.method=='POST':
          new_user_name=request.POST.get('username')
          new_email_address=request.POST.get('email')
          new_phone_number=request.POST.get('phone')
          new_user_address=request.POST.get('address')
          
          try:
               new_user_profile_image = request.FILES["profileimage"]
          except:
               new_user_profile_image=None
          
          if new_user_name =="":
               new_user_name=None
          
          if new_email_address=="":
               new_email_address=None
          
          if new_phone_number=="":
               new_phone_number=None
          
          if new_user_address=="":
               new_user_address=None
                    
          user= Userdetails.objects.get(user_name=request.session.get('userindicator'))
          
          if new_user_name:
               request.session['userindicator']= new_user_name
               user.user_name=new_user_name 
               user.save()
               
          if new_email_address:
               user.user_email=new_email_address
               user.save()
               
          if new_phone_number:
               user.user_phone=new_phone_number
               user.save()
               
          if new_user_address:
               user.user_address=new_user_address
               user.save()
               
          if new_user_profile_image:
               user.user_profile_image=new_user_profile_image
               user.save()

     return redirect("Bidbay1:Bidbay_profile")    

def place_bid(request):
    

     item_id=request.POST.get('item_id')
     
     bid_amount=int(request.POST.get('bid_amount'))
     
     item_details=Items.objects.get(item_id=item_id)
     item_current_bid_amount=int(item_details.item_final_price)
     
     if bid_amount > item_current_bid_amount : 
          
          item_details.item_final_price = bid_amount
          
          bid_user_id=Userdetails.objects.get(user_name=request.session.get('userindicator'))
          
          item_details.item_buyer_id = bid_user_id
          
          item_details.save()
          
          get_user_id=item_details.user_id.user_id
     
          user_ads=len(Items.objects.filter(user_id=get_user_id))
          
          get_user_details=Userdetails.objects.get(user_id=get_user_id)
          
          get_image_list=Images.objects.filter(item_id=item_details.item_id)
          
          image_url_list=[]
          
          item_details_list=[item_details.item_name ,item_details.item_description,item_details.item_id,
                         ((item_details.item_expiry_date-timezone.now()).days) , item_details.item_final_price,(int(((item_details.item_expiry_date-timezone.now()).total_seconds()))//3600)%24]
          
          user_details_list=[get_user_details.user_profile_image.url , get_user_details.user_name , user_ads,
                                   get_user_details.user_date_joined.strftime('%Y-%m-%d'), get_user_details.user_phone ,
                                   get_user_details.user_address]
     
          for items in get_image_list:
               image_url_list.append(items.image_file.url)
          
          details_list=[image_url_list,user_details_list,item_details_list]
          
          return{'data':details_list, 'bid_data':'0'} 
                    
          
     elif  bid_amount <= item_current_bid_amount:
          
          get_user_id=item_details.user_id.user_id
     
          user_ads=len(Items.objects.filter(user_id=get_user_id))
          
          get_user_details=Userdetails.objects.get(user_id=get_user_id)
          
          get_image_list=Images.objects.filter(item_id=item_details.item_id)
          
          image_url_list=[]
          
          item_details_list=[item_details.item_name ,item_details.item_description,item_details.item_id,
                         ((item_details.item_expiry_date-timezone.now()).days) , item_details.item_final_price]
          
          user_details_list=[get_user_details.user_profile_image.url , get_user_details.user_name , user_ads,
                                   get_user_details.user_date_joined.strftime('%Y-%m-%d'), get_user_details.user_phone ,
                                   get_user_details.user_address]
     
          for items in get_image_list:
               
               image_url_list.append(items.image_file.url)
          
          details_list=[image_url_list,user_details_list,item_details_list]
          
          return{'data':details_list, 'bid_data':'1'}          

def match_entered_pw_with_pw_in_db(request, username,password):
     entered_password=password
     db_password=fetch_pw_and_decrypt(username)
     
     if entered_password==db_password:
          return True
     else:
          return False
     

def fetch_pw_and_decrypt(username):
      try:
        # Load the encryption key from the file
        file_path = os.path.join(settings.BASE_DIR, 'Bidbay1', 'static', 'Bidbay1', 'sample.txt')
        with open(file_path, 'rb') as file:
            key = file.read().strip()  # Ensure the key is correctly read

        # Ensure the key is the correct length for Fernet (32 bytes)
        if len(key) != 44:
            raise ValueError("Invalid key length. Ensure the key is 32 bytes URL-safe base64-encoded string.")

        f = Fernet(key)

        # Fetch the encrypted password from the database
        password_obj = Userdetails.objects.get(user_name=username)
        encrypted_password = password_obj.user_pwd  # Ensure the password is in bytes
        x=encrypted_password.encode()

        # Decrypt the password
        
        decrypted_password = f.decrypt(x).decode() 

        return decrypted_password

      except Exception as e:
        print(f"Exception occurred: {e}")
        raise e
   
def get_item_detail_for_deleting(request):
     
     global page_state_variable
          
     var_user_id=None
     
     user=Userdetails.objects.get(user_name=request.session.get('userindicator'))
     
     var_user_id=user.user_id

     user_id=var_user_id
     
     item_objects_main=Items.objects.filter(user_id=user_id)
          
     current_item_details_list=[]
     
     for item in item_objects_main:
          item_details=[]
          item_id=item.item_id
          if(item.item_expiry_date > timezone.now()):
               item_details.append(item_id)
               image_objects=Images.objects.filter(item_id=item_id)
               
               for image in image_objects:
                    item_details.append(image.image_file.url)
                    break
               item_details.append(item.item_name)
               item_details.append((item.item_expiry_date-timezone.now()).days)
               item_details.append(item.item_final_price)
               item_details.append(int((((item.item_expiry_date-timezone.now()).total_seconds()) // 3600)%24))
               item_details.append(item.item_auction_type)
                    
               current_item_details_list.append(item_details)
               
     for items in current_item_details_list:
          if(items[6] == 'live' ):
               
               live_item=Items.objects.get(item_id=items[0])
               
               time_remaining=live_item.item_expiry_date - timezone.now()
               
               hours = time_remaining.seconds // 3600
               minutes = (time_remaining.seconds % 3600) // 60
               seconds = time_remaining.seconds % 60
               data =[hours , minutes , seconds]
               items.append(data)
               
     return current_item_details_list
               
def delete_items(request):
     if request.method == 'POST':
          
        # Initialize a dictionary to store the input values
          input_values = {}

        # Iterate through POST data to find keys that start with "name_"
          for key in request.POST:
               if key.startswith('normal_checkbox_'):
                # Add the key-value pair to the dictionary
                    input_values[key] = request.POST[key]
               if key.startswith('live_checkbox_'):
                    input_values[key] = request.POST[key]
          
          item_ids=[]
          
          for key in input_values.keys():
               item_ids.append(key[-1])
           
          for item_id in item_ids:    
               Items.objects.filter(item_id=item_id).delete()
          
          return redirect("Bidbay1:Bidbay_profile")

def get_detail_for_bought_item(request):
     
     selected_item_id = request.POST.get("this_item_id") 
            
     item_details=Items.objects.get(item_id=selected_item_id) 
     
     get_user_id=item_details.user_id.user_id
     
     user_ads=len(Items.objects.filter(user_id=get_user_id))
     
     get_user_details=Userdetails.objects.get(user_id=get_user_id)
     
     get_image_list=Images.objects.filter(item_id=selected_item_id)
     
     image_url_list=[]
     
     item_details_list=[item_details.item_name ,item_details.item_description,
                         item_details.item_id, item_details.item_final_price,item_details.item_expiry_date.strftime('%Y-%m-%d')]
     
     user_details_list=[get_user_details.user_profile_image.url , get_user_details.user_name , user_ads,
                                   get_user_details.user_date_joined.strftime('%Y-%m-%d'),get_user_details.user_phone,get_user_details.user_address
                                   ]
     
     for items in get_image_list:
          image_url_list.append(items.image_file.url)
               
     details_list=[image_url_list,user_details_list,item_details_list]     

     return details_list
     

def get_detail_for_sold_item(request):
          
          selected_item_id = request.POST.get("this_item_id") 
            
          item_details=Items.objects.get(item_id=selected_item_id) 
          
          get_user_id=item_details.user_id.user_id
          
          user_ads=len(Items.objects.filter(user_id=get_user_id))
          
          get_user_details=Userdetails.objects.get(user_id=get_user_id)
          
          get_image_list=Images.objects.filter(item_id=selected_item_id)
          
          image_url_list=[]
          
          item_details_list=[item_details.item_name ,item_details.item_description,
                             item_details.item_id, item_details.item_final_price,item_details.item_expiry_date.strftime('%Y-%m-%d')]
          
          user_details_list=[get_user_details.user_profile_image.url , get_user_details.user_name , user_ads,
                                    get_user_details.user_date_joined.strftime('%Y-%m-%d'),
                                    ]
         
          for items in get_image_list:
               image_url_list.append(items.image_file.url)
               
          buyer_details_list=[]
          
          buyer_id=item_details.item_buyer_id.user_id
          
          buyer_detail=Userdetails.objects.get(user_id=buyer_id)
          
          buyer_details_list.append(buyer_detail.user_phone)
          
          buyer_details_list.append(buyer_detail.user_name)
                    
          details_list=[image_url_list,user_details_list,item_details_list,buyer_details_list]     

          return details_list
          
          # request.session['data']={'data':details_list}          
          
          # return redirect("Bidbay1:Bidbay_itemdetails") 

def get_details_for_edit_profile_info(request):
     
     x=Userdetails.objects.get(user_name=request.session.get('userindicator'))
     user_id=x.user_id
     user_details=Userdetails.objects.get(user_id=user_id)
     user_profile_image=user_details.user_profile_image.url
     user_fname=user_details.user_fname
     user_lname=user_details.user_lname
     user_name=user_details.user_name
     user_email=user_details.user_email
     user_phone=user_details.user_phone
     user_address=user_details.user_address
     user_details_list=[user_fname,user_lname,user_email,user_name,user_phone,user_address,user_profile_image]
     
     return user_details_list

def store_item_details_and_images(request):
     
     if request.method=="POST":
          x=Userdetails.objects.get(user_name=request.session.get('userindicator'))
          user_id=x
          item_name=request.POST.get("item_name")
          item_description=request.POST.get("item_description")
          item_category=request.POST.get("item_category")
          item_starting_price= request.POST.get("item_starting_price")
          item_images= request.FILES.getlist('file')
          item_auction_type=request.POST.get("item_auction_type")
          if item_auction_type=='Normal':
               get_date_time=timezone.now()
               item_upload_date=get_date_time
               item_expiry_date=(item_upload_date + timedelta(days=10))
               save_details=Items(user_id=user_id,item_name=item_name, item_description=item_description,
                              item_auction_type=item_auction_type , item_starting_price=item_starting_price,
                              item_final_price=item_starting_price,
                              item_upload_date=item_upload_date , 
                              item_category=item_category,item_expiry_date=item_expiry_date)
               save_details.save()
          else:
               get_date=timezone.now()
               one_hour_later = get_date + timedelta(hours=1)
               save_details=Items(user_id=user_id,item_name=item_name, item_description=item_description,
                              item_auction_type=item_auction_type , item_starting_price=item_starting_price,
                              item_final_price=item_starting_price ,
                              item_upload_date=get_date , 
                              item_category=item_category,item_expiry_date=one_hour_later)
               save_details.save()
               
               
          y=Items.objects.order_by('item_id').last()
          
          for img in item_images:
                save_images=Images(user_id=user_id,item_id=y,image_file=img)
                save_images.save()
                
          if y.item_auction_type == 'live':
               room_detail=Room(room_name = y)      
               room_detail.save()
          
          return redirect("Bidbay1:Bidbay_home")
          
def get_item_and_user_details_for_profilepage(request):
     
          global page_state_variable
          
          var_user_id=None
          
          user=Userdetails.objects.get(user_name=request.session.get('userindicator'))
          var_user_id=user.user_id
     
          user_id=var_user_id
              
          get_user_details=Userdetails.objects.get(user_id=user_id)
          
          user_ads=len(Items.objects.filter(user_id=user_id))
          
          user_details_list=[get_user_details.user_profile_image.url , get_user_details.user_name , user_ads,
                                    get_user_details.user_fname,get_user_details.user_lname, get_user_details.user_phone ,
                                    get_user_details.user_address,get_user_details.user_email,
                                    get_user_details.user_date_joined.strftime('%Y-%m-%d')]
          
          item_objects_main=Items.objects.filter(user_id=user_id)
               
          current_item_details_list=[]
          
          sold_item_details_list=[]
          
          for item in item_objects_main:
               item_details=[]
               item_id=item.item_id
               if(item.item_expiry_date > timezone.now()):
                    item_details.append(item_id)
                    image_objects=Images.objects.filter(item_id=item_id)
                    
                    for image in image_objects:
                         item_details.append(image.image_file.url)
                         break
                    item_details.append(item.item_name)
                    item_details.append((item.item_expiry_date-timezone.now()).days)
                    item_details.append(item.item_final_price)
                    item_details.append(int((((item.item_expiry_date-timezone.now()).total_seconds()) // 3600)%24))
                    item_details.append(item.item_auction_type)
                         
                    current_item_details_list.append(item_details)
                    
          for items in current_item_details_list:
               if(items[6] == 'live' ):
                    
                    live_item=Items.objects.get(item_id=items[0])
                    
                    time_remaining=live_item.item_expiry_date - timezone.now()
                    
                    hours = time_remaining.seconds // 3600
                    minutes = (time_remaining.seconds % 3600) // 60
                    seconds = time_remaining.seconds % 60
                    data =[hours , minutes , seconds]
                    items.append(data)
                    
          for item in item_objects_main:
               item_details=[]
               item_id=item.item_id
               if((item.item_expiry_date < timezone.now() and (item.item_starting_price != item.item_final_price))):
                    item_details.append(item_id)
                    image_objects=Images.objects.filter(item_id=item_id)
                    for image in image_objects:
                         item_details.append(image.image_file.url)
                         break
                    item_details.append(item.item_name)
                    item_details.append(item.item_final_price)
                    item_details.append(item.item_expiry_date.strftime('%Y-%m-%d'))
                    sold_item_details_list.append(item_details)
          
          bought_item_details_list=[]
          
          item_objects_main_buy = Items.objects.filter(item_buyer_id=user_id)
          
          for item in item_objects_main_buy:
               item_details=[]
               item_id=item.item_id
               if((item.item_expiry_date < timezone.now()) and (item.item_starting_price != item.item_final_price)):
                    item_details.append(item_id)
                    image_objects=Images.objects.filter(item_id=item_id)
                    for image in image_objects:
                         item_details.append(image.image_file.url)
                         break
                    item_details.append(item.item_name)
                    item_details.append(item.item_final_price)
                    item_details.append(item.item_expiry_date.strftime('%Y-%m-%d'))
                    bought_item_details_list.append(item_details)
          
          combined_list=[user_details_list, current_item_details_list, sold_item_details_list,bought_item_details_list]
          
          return {'data4':combined_list}
 

     
    
def store_username_and_encryptedpwd(request):
     if request.method=='POST':
          name=request.POST.get("username")
          fname=request.POST.get("fname")
          lname=request.POST.get("lname")
          email=request.POST.get("email")
          password=request.POST.get("password")
          birthdate=request.POST.get("DOB")
          phone=request.POST.get("phone")
          address=request.POST.get("address")
          date_joined = date.today()
          profile_image = request.FILES["image"]
          a=read_pw_and_encrypt(password).decode()
          request.session['prevent_event_action']='0'
          if Userdetails.objects.filter(user_name=name).exists():
               request.session['prevent_event_action']='1'
               return redirect("Bidbay1:Bidbay_register")
          else:
               save_details=Userdetails(user_name=name,user_fname=fname,user_lname=lname,
                                        user_email=email,user_pwd=a,user_DOB=birthdate,
                                        user_phone=phone,
                                        user_address=address,user_date_joined=date_joined,user_profile_image=profile_image)
               save_details.save()
               request.session['prevent_event_action']='0'
               return redirect ("Bidbay1:Bidbay_login")
        

def read_pw_and_encrypt(password):
    file_path = os.path.join(settings.BASE_DIR,'Bidbay1', 'static', 'Bidbay1', 'sample.txt')
    try:
        with open(file_path, 'rb') as file:
            file_content = file.read()
            f=Fernet(file_content)
            y=f.encrypt(password.encode())            
            
    except FileNotFoundError:
        raise HttpResponse("File does not exist")

    return y

def get_user_profile_pic(request):
     image=Userdetails.objects.get(user_name=request.session.get('userindicator')).user_profile_image
     return [image.url,image]

def get_item_details_for_item_list_page(request):
         if request.method=="POST":
              category_name=request.POST.get('category_name')  
              item_list_of_category=Items.objects.filter(item_category=category_name)
              item_ids=[]
              item_name=[]
              item_description=[]
              item_price=[]
              item_remaining_time_days=[]
              item_first_image_url=[]
              item_remaining_hours=[]
              item_auction_type=[]
              
              for items in item_list_of_category:
                   if ((items.item_expiry_date > timezone.now())):
                        
                              item_id=items.item_id
                              item_ids.append(item_id)
                              image_object_list=list(Images.objects.filter(item_id=item_id))
                              for obj in image_object_list:
                                   item_first_image_url.append(obj.image_file.url)
                                   break
                              item_name.append(items.item_name)
                              item_price.append(items.item_final_price)
                              item_remaining_time_days.append((items.item_expiry_date-timezone.now()).days)
                              item_remaining_hours.append(int((((items.item_expiry_date-timezone.now()).total_seconds()) // 3600)%24))
                              item_description.append(items.item_description)
                              item_auction_type.append(items.item_auction_type)
                              
              combined_list = [list(t) for t in zip(item_ids,item_name,item_description ,item_price, item_remaining_time_days, item_first_image_url,item_remaining_hours,item_auction_type)]
              
              for item in combined_list:
                   if item[7] == 'live':
                       item_detail=Items.objects.get(item_id=item[0])
                       time_remaining = item_detail.item_expiry_date - timezone.now()  # Calculate time remaining
                       hours = time_remaining.seconds // 3600
                       minutes = (time_remaining.seconds % 3600) // 60
                       seconds = time_remaining.seconds % 60
                       data =[hours , minutes , seconds]
                       item.append(data) 
                       
              request.session['data2'] = {'data2':combined_list,'data21':category_name}
              
              request.session['use_data2'] = True
              
              return redirect("Bidbay1:Bidbay_itemlist")

def get_newdeals_item_details_in_homepage():
     Items_list=Items.objects.order_by('-item_id')
     item_ids=[]
     item_name=[]
     item_price=[]
     item_remaining_time_days=[]
     item_remaining_hours=[]
     item_first_image=[]
     for items in Items_list:
          if ((items.item_expiry_date > timezone.now()) and (items.item_auction_type == 'Normal') ):
               if(((items.item_expiry_date-timezone.now()).days)>5):
                    item_id=items.item_id
                    item_ids.append(item_id)
                    image_object_list=list(Images.objects.filter(item_id=item_id))
                    for obj in image_object_list:
                         item_first_image.append(obj.image_file.url)
                         break
                    item_name.append(items.item_name)
                    item_price.append(items.item_final_price)
                    item_remaining_time_days.append((items.item_expiry_date-timezone.now()).days)
                    item_remaining_hours.append(int((((items.item_expiry_date-timezone.now()).total_seconds()) // 3600)%24))          
     
     combined_list = [list(t) for t in zip(item_ids,item_name, item_price, item_remaining_time_days, item_first_image,item_remaining_hours)]
    
     return combined_list

def get_endingsoon_item_details_in_homepage():
     
     Items_list=Items.objects.order_by('item_id')
     item_ids=[]
     item_name=[]
     item_price=[]
     item_remaining_time_days=[]
     item_remaining_hours=[]
     item_first_image=[]
     for items in Items_list:
          if ((items.item_expiry_date > timezone.now()) and (items.item_auction_type == 'Normal')):
               
               # pachi make it less than equal to 3
               
               if(((items.item_expiry_date-timezone.now()).days) <= 5 ): 
                    item_id=items.item_id
                    item_ids.append(item_id)
                    image_object_list=list(Images.objects.filter(item_id=item_id))
                    for obj in image_object_list:
                         item_first_image.append(obj.image_file.url)
                         break
                    item_name.append(items.item_name)
                    item_price.append(items.item_final_price)
                    item_remaining_time_days.append((items.item_expiry_date-timezone.now()).days)
                    item_remaining_hours.append(int((((items.item_expiry_date-timezone.now()).total_seconds()) // 3600)%24))
     
     combined_list = [list(t) for t in zip(item_ids,item_name, item_price, item_remaining_time_days, item_first_image,item_remaining_hours)]
     
     return combined_list


def get_livebid_item_details_in_homepage():
     Items_list=Items.objects.order_by('item_id')
     item_ids=[]
     item_name=[]
     item_price=[]
     
     item_first_image=[]
     for items in Items_list:
          if ((items.item_expiry_date > timezone.now()) and (items.item_auction_type == 'live')):  
               
               # pachi make it less than equal to 3
                
               item_id=items.item_id
               item_ids.append(item_id)
               image_object_list=list(Images.objects.filter(item_id=item_id))
               for obj in image_object_list:
                    item_first_image.append(obj.image_file.url)
                    break
               item_name.append(items.item_name)
               item_price.append(items.item_final_price)
                    
     
     combined_list = [list(t) for t in zip(item_ids,item_name, item_price,  item_first_image)]
     
     return combined_list
                    

def get_liveitem_detail(request):
     if request.method=="POST":
          
          selected_item_id = request.POST.get("live_item_id") 
          
          item_details=Items.objects.get(item_id=selected_item_id) 
                    
          get_user_id=item_details.user_id.user_id          
          
          user_ads=len(Items.objects.filter(user_id=get_user_id))
          
          get_user_details=Userdetails.objects.get(user_id=get_user_id)
          
          get_image_list=Images.objects.filter(item_id=selected_item_id)
          
          # for countdown
          
          item_expiry_time=[]
          
          if((item_details.item_expiry_date>timezone.now()) and item_details.item_auction_type=='live'):
                    time_remaining = item_details.item_expiry_date - timezone.now()  # Calculate time remaining
                    hours = time_remaining.seconds // 3600
                    minutes = (time_remaining.seconds % 3600) // 60
                    seconds = time_remaining.seconds % 60
                    
                    item_expiry_time.append(hours)
                    item_expiry_time.append(minutes)
                    item_expiry_time.append(seconds)
               
          # end countdown
          
          
          image_url_list=[]
          
          item_details_list=[item_details.item_name ,item_details.item_description,item_details.item_id,
                              item_details.item_final_price]
          
          user_details_list=[get_user_details.user_profile_image.url , get_user_details.user_name , user_ads,
                                    get_user_details.user_date_joined.strftime('%Y-%m-%d'), get_user_details.user_phone ,
                                    get_user_details.user_address]
         
          for items in get_image_list:
               image_url_list.append(items.image_file.url)
          
          details_list=[image_url_list,user_details_list,item_details_list,item_expiry_time]
          
          return {'data1':details_list}
          
          
def get_item_details(request):
     
     if request.method=='POST':
          
          selected_item_id = request.POST.get("this_item_id") 
            
          item_details=Items.objects.get(item_id=selected_item_id) 
          
          get_user_id=item_details.user_id.user_id
          
          user_ads=len(Items.objects.filter(user_id=get_user_id))
          
          get_user_details=Userdetails.objects.get(user_id=get_user_id)
          
          get_image_list=Images.objects.filter(item_id=selected_item_id)
          
          image_url_list=[]
          
          item_details_list=[item_details.item_name ,item_details.item_description,item_details.item_id,
                             ((item_details.item_expiry_date-timezone.now()).days) , item_details.item_final_price,(int((((item_details.item_expiry_date-timezone.now()).total_seconds()) // 3600)%24))]
          
          user_details_list=[get_user_details.user_profile_image.url , get_user_details.user_name , user_ads,
                                    get_user_details.user_date_joined.strftime('%Y-%m-%d'), get_user_details.user_phone ,
                                    get_user_details.user_address]
         
          for items in get_image_list:
               image_url_list.append(items.image_file.url)
               
          get_operating_user_id=Userdetails.objects.get(user_name=request.session.get('userindicator')).user_id
          
          get_item_upload_user_id=item_details.user_id.user_id
          
          details_list=[image_url_list,user_details_list,item_details_list] 
          
          if (get_operating_user_id == get_item_upload_user_id):
               details_list.append(1)    
          

          
          return {'data':details_list}         
          
              
                    
def countdown_timer(request):
     Items_list=Items.objects.order_by('item_id')
     item_expiry_time=[]
     for item in Items_list:
          if((item.item_expiry_date>timezone.now()) and item.item_auction_type=='live'):
               if item:
                    time_remaining = item.item_expiry_date - timezone.now()  # Calculate time remaining
                    hours = time_remaining.seconds // 3600
                    minutes = (time_remaining.seconds % 3600) // 60
                    seconds = time_remaining.seconds % 60
                    data =[hours , minutes , seconds]
                    item_expiry_time.append(data)
               # else:
               #      data = {
               #           'name': "No Event",
               #           'hours': 0,
               #           'minutes': 0,
               #           'seconds': 0
               #      }  
     return item_expiry_time   
           
def reset_user_id_sequence():
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='Bidbay1_message';")
        
def create_key_and_write_in_file():
     file_path = os.path.join(settings.BASE_DIR,'Bidbay1', 'static', 'Bidbay1', 'sample.txt')
     key = Fernet.generate_key()
     with open(file_path, "wb") as key_file:
          key_file.write(key)
          key_file.close()

    
