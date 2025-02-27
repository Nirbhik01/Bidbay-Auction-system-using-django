from django.db import models

PAYMENT_STATUS = (
    ('Paid', 'Paid'),
    ('Not Paid', 'Not Paid'),
    ('Processing', 'Processing')
)

class Userdetails(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    user_name = models.CharField(max_length=100)
    user_fname=models.CharField(max_length=50)
    user_lname=models.CharField(max_length=50)
    user_email=models.CharField(max_length=50)
    user_pwd=models.CharField(max_length=1500)
    user_DOB=models.DateField()
    user_phone=models.IntegerField(max_length=100)
    user_address=models.CharField(max_length=100)
    user_date_joined=models.DateField()
    user_profile_image=models.ImageField(upload_to='Bidbay1/static/Bidbay1/profile_images',null=True, blank=True)   
    
    def __str__(self):
       return self.user_name
    
class Items(models.Model):
    user_id=models.ForeignKey(Userdetails,null=False, blank=False,on_delete=models.CASCADE,related_name='items_uploaded')
    item_id=models.BigAutoField(primary_key=True)
    item_name=models.CharField(max_length=100)
    item_description=models.TextField(max_length=1500)
    item_auction_type=models.CharField(max_length=20)
    item_starting_price=models.IntegerField(null=False,blank=False)
    item_final_price=models.IntegerField()
    item_upload_date=models.DateTimeField()
    item_category=models.CharField(max_length=20)
    item_expiry_date=models.DateTimeField()
    item_buyer_id=models.ForeignKey(Userdetails,null=True, blank=True,on_delete=models.SET_NULL,related_name='items_bought')
    item_payment_status=models.CharField(max_length=100,choices=PAYMENT_STATUS,default="Processing")
    
    def __str__(self):
        return f"{self.item_id}-{self.item_name}"
    
class Images(models.Model):
    image_id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(Userdetails, null=False, blank=False,on_delete=models.CASCADE)
    item_id=models.ForeignKey(Items, null=False, blank=False,on_delete=models.CASCADE)
    image_file=models.ImageField(upload_to='Bidbay1/static/Bidbay1/product_images')
    
    def __str__(self):
        return f"Image :- {self.image_id} , User:- {self.user_id}, Item:- {self.item_id}"
    
class Room(models.Model):
    room_id=models.AutoField(primary_key=True)
    room_name=models.ForeignKey(Items,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Room:-{self.room_id} , Item:- {self.room_name}"

class Message(models.Model):
    room_name=models.ForeignKey (Room,on_delete=models.CASCADE)
    sender=models.ForeignKey (Userdetails,on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    
    def __str__(self):
        return f"Room:-{self.room_name} , Sender:- {self.sender}"
    
    
class current_bids(models.Model):
    bid_id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(Userdetails, on_delete=models.CASCADE,null=True,blank=True)
    item_id=models.ForeignKey(Items, on_delete=models.CASCADE,null=True,blank=True)
    


# Create your models here.
