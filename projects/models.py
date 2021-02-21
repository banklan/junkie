from django.db import models
from django.conf import settings
from datetime import datetime
from django.utils import timezone
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.utils.text import slugify

import secrets

from profiles.models import CustomUser

from django_resized import ResizedImageField


class Category(models.Model):
	name = models.CharField(max_length=100)
	slug = models.SlugField()
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']

# create a slug while saving model
def pre_save_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)

pre_save.connect(pre_save_slug, sender=Category)


class Project(models.Model):
	author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	beneficiary = models.CharField(max_length=100, blank=True, null=True)
	title = models.CharField(max_length=255, unique=True)
	slug = models.SlugField()
	details = models.TextField()
	goal = models.DecimalField(max_digits=9, decimal_places=2)
	expiry = models.DateTimeField()
	can_update_expiry = models.BooleanField(default=True)
	old_expiry = models.DateTimeField(default=datetime.now)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	is_approved = models.BooleanField(default=False)
	is_featured = models.BooleanField(default=False)
	view_count = models.IntegerField(default=0)
	paid = models.BooleanField(default=False)
	image = ResizedImageField(size=[520, 400], quality=85, upload_to="projects", blank=True, null=False)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-created']

	def published_date(self):
		pub = self.created
		mod = pub.strftime("%B %d, %Y")
		return mod

	def expiry_date(self):
		exp = self.expiry
		mod = exp.strftime("%B %d, %Y")
		return mod

	def incrementViewCount(self):
		self.view_count += 1
		self.save()

	def creator(self):
		return self.author.first_name + ' ' + self.author.last_name

	def donations(self):
		donations = Donation.objects.filter(project=self)
		return donations

	def updates(self):
		updates = Update.objects.filter(project=self)
		return updates

	def get_image(self):
		if self.image:
			return self.image.url
		return settings.MEDIA_URL + 'projects/no-image.png'

	def total_donations(self):
		total = 0
		donations = Donation.objects.filter(project=self)
		for donation in donations:
			total = total + donation.amount
		if len(donations) > 0:
			return int(total)
		else:
			return 0

	def percent_raised(self):
		total = 0
		donations = Donation.objects.filter(project=self)
		for donation in donations:
			total = total + donation.amount
		if len(donations) > 0:
			perc = int(round(total / self.goal * 100))
			return perc
		return 0

	def to_expire(self):
		today = datetime.now().date()
		d1 = self.expiry.date()
		delta = d1 - today
		return delta.days

	@property
	def status(self):
		if self.total_donations == self.goal:
			return 'Accomplished'
		return 'Not Accomplished'


	def followers(self):
		followers = Follow.objects.filter(project=self)
		return followers


class Donation(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	name = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	show_name = models.BooleanField(default=True, blank=True, null=True)
	amount = models.DecimalField(max_digits=9, decimal_places=2)
	comment = models.CharField(max_length=300, null=True, blank=True)
	trx_id = models.IntegerField(default=0)
	trx_ref = models.CharField(max_length=20, null=True, blank=True)
	trx_msg = models.CharField(max_length=40, null=True, blank=True)
	is_approved = models.BooleanField(default=False)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name.first_name + ' ' + self.name.last_name

	class Meta:
		ordering = ['-date']

	def date_donated(self):
		dt = self.date
		mod = dt.strftime("%b %d, %Y")
		return mod

	def backer(self):
		if self.show_name == True:
			return self.name.first_name + ' ' + self.name.last_name
		return 'Anonymous'

	# def backer_pic(self):
	# 	if self.backer == 'Anonymous':
	# 		picture = 'http://localhost:8000/media/profiles/no_image.jpg'
	# 		return picture



class Update(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="update")
	title = models.CharField(max_length=150, unique=True)
	details = models.TextField(max_length=600)
	image = ResizedImageField(size=[380, 300], quality=85, upload_to="updates", blank=True, null=False)
	is_approved = models.BooleanField(default=False)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-date']

	def published(self):
		pub = self.date
		mod = pub.strftime("%B %d, %Y")
		return mod

	def get_image(self):
		if self.image:
			return self.image.url
		return settings.MEDIA_URL + 'updates/no-image.png'


# delete image related to update when an update object is deleted
@receiver(pre_delete, sender=Update)
def update_delete(sender, instance, **kwargs):
    instance.image.delete(False)




class UpdateImage(models.Model):
	update = models.ForeignKey(Update, on_delete=models.CASCADE)
	image = ResizedImageField(size=[520, 400], quality=85, upload_to="updates", blank=True, null=False)
	date = models.DateTimeField(auto_now_add=True)

	# def __str__(self):
	# 	return self.update


class ProjectReport(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	title = models.CharField(max_length=150)
	details = models.TextField(max_length=400)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title


class Follow(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.follower.first_name + ' ' + self.follower.last_name

	class Meta:
		unique_together = ['project', 'follower']
		ordering = ['-created']

	def date_followed(self):
		pub = self.created
		mod = pub.strftime("%B %d, %Y")
		return mod



class BankDetail(models.Model):
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
	bank = models.CharField(max_length=20)
	account_type = models.CharField(max_length=10)
	account_number = models.IntegerField()
	account_name = models.CharField(max_length=255)
	id_card = ResizedImageField(size=[420, 300], quality=85, upload_to="identification", blank=True, null=False)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.first_name + ' '+ self.user.last_name

	class Meta:
		ordering = ['user']

@receiver(pre_delete, sender=BankDetail)
def bank_details_delete(sender, instance, **kwargs):
    instance.id_card.delete(False)



class Bank(models.Model):
	name = models.CharField(max_length=50)
	short_name = models.CharField(max_length=20)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']


class PasswordReset(models.Model):
    email = models.EmailField(null=True)
    token = models.CharField(max_length=200, default=secrets.token_hex(88))
    expiry = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



class SuccessStory(models.Model):
	project = models.OneToOneField(Project, on_delete=models.CASCADE)
	title = models.CharField(max_length=150)
	details = models.TextField(max_length=800)
	is_approved = models.BooleanField(default=False)
	is_featured = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['created']


	def date(self):
		pub = self.created
		mod = pub.strftime("%B %d, %Y")
		return mod



class SuccessStoryImage(models.Model):
	story = models.ForeignKey(SuccessStory, on_delete=models.CASCADE)
	image = ResizedImageField(size=[520, 400], quality=85, upload_to="success", blank=True, null=False)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.story


class EnquiryContact(models.Model):
    email = models.EmailField()
    f_name = models.CharField(max_length=30, blank=True, null=True)
    l_name = models.CharField(max_length=30, blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    subject = models.CharField(max_length=100, blank=True, null=True)
    message = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.email


class WithdrawRequest(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	project = models.OneToOneField(Project, on_delete=models.CASCADE)
	amount = models.DecimalField(max_digits=9, decimal_places=2)
	is_approved = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.project.title

	class Meta:
		ordering = ['created']

	def date(self):
		pub = self.created
		mod = pub.strftime("%B %d, %Y")
		return mod











