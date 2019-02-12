from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import * 
from albums.models import Album
@receiver(post_save, sender=OrderItem)
def item_order_receiver(sender,instance,**kwargs):
	"""Modify total to be payed"""
	# Change total_payed
	album = Album.objects.get(id = instance.album.id)
	total = album.price * instance.quantity
	order = Order.objects.get(id = instance.order.id)
	new_count = order.total_payed + total
	order.total_payed = new_count
	order.save()
	# update total sales and album quantity
	album.total_sales = album.total_sales + total
	album.quantity = album.quantity - instance.quantity

	album.save()