from django.contrib import admin
from django.urls import path,include
from .views import *

app_name='Bidbay1'

urlpatterns = [
   path('loginpage/',Bidbay_login,name='Bidbay_login'),
   path('registerpage/',Bidbay_register,name='Bidbay_register'),
   path('homepage/',Bidbay_home,name='Bidbay_home'),
   path('uploaditempage/',Bidbay_uploaditem,name='Bidbay_uploaditem'),
   path('itemdetailspage/',Bidbay_itemdetails,name='Bidbay_itemdetails'),
   path('itemlistpage/', Bidbay_itemlist, name='Bidbay_itemlist'),


   path('create_payment/<int:item_id>/',create_payment, name='create_payment'),
   path('execute_payment/<int:item_id>/',execute_payment, name='execute_payment'),
   path('payment_failed/<int:item_id>',payment_failed, name='payment_failed'),
   path('liveauctionpage/<str:room_name>/<str:user_name>/',Bidbay_liveauction,name='Bidbay_liveauction'),
   path('deletingprofile',delete_profile,name='delete_profile'),
   path('profilepage/',Bidbay_profile,name='Bidbay_profile'),
   
   path('authenticating/',login_user_authentication,name='login_user_authentication'),
   path("storingusernameandpwd",store_username_and_encryptedpwd,name="store_username_and_encryptedpwd"),
   path('storingitemdetails/',store_item_details_and_images,name='store_item_details_and_images'),
   path('fetchingitemdetails/',get_item_details,name='get_item_details'),
   path('fetchingitemlist/',get_item_details_for_item_list_page,name="get_item_details_for_item_list_page"),
   path('gotoliveauctiondetails/',get_liveitem_detail,name="get_liveitem_detail"),
   path('get_item_and_user_derails_for_profilepage/',get_item_and_user_details_for_profilepage,name="get_item_and_user_details_for_profilepage"),
   path('logout/',logout_functionality,name="logout_functionality"),
   path('placingbid/',place_bid,name="place_bid"),
   path('filtering/',filtering_functionality,name="filtering_functionality"),
   path('searching/',search_functionality,name="search_functionality"),
   path('editprofileinfo/',Bidbay_editprofileinfo,name="Bidbay_editprofileinfo"),
   path('savingchanges/',save_changes_to_profile_details,name="save_changes_to_profile_details"),
   path('solditemdetail/',Bidbay_solditemdetail,name="Bidbay_solditemdetail"), 
   path('boughtitemdetail/',Bidbay_boughtitemdetail,name="Bidbay_boughtitemdetail"),
   path('deleteitems/',Bidbay_deleteitems,name="Bidbay_deleteitems"),
   path('deletingitems/',delete_items,name="delete_items"),
   path('save_bid',place_bid_for_live_auction,name='place_bid_for_live_auction')
]

admin.site.site_header = "Bidbay Admin Pannel"
admin.site.site_title = "Bidbay Admin Portal"
admin.site.index_title = "Welcome to Bidbay Admin"