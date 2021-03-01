from django.conf import settings
from datetime import date, datetime, timedelta
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import secrets
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from .models import (
	Category, Project, Donation, ProjectReport, Update, UpdateImage, Follow, BankDetail, Bank, 
	PasswordReset, SuccessStory, EnquiryContact, WithdrawRequest
)
from profiles.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
	fullname = serializers.CharField(source="get_fullname")
	class Meta:
		model = get_user_model()
		fields = ['id', 'first_name', 'last_name', 'fullname', 'email', 'phone_no', 'location', 'picture']


########################Generate Tokens for all existing users########################
# Users = get_user_model().objects.all()
# for user in Users:
# 	Token.objects.get_or_create(user=user)



class TokenSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Token
        fields = ('key', 'user')



class DonationSerializer(serializers.ModelSerializer):
	name = UserSerializer(read_only=True)
	amount = serializers.DecimalField(max_digits=9, decimal_places=2)
	date = serializers.DateTimeField(source='date_donated')
	backer = serializers.CharField()
	trx_id =serializers.IntegerField()
	trx_ref = serializers.CharField()
	trx_msg = serializers.CharField()
	class Meta:
		model = Donation
		fields = ['name', 'amount', 'comment', 'date', 'backer', 'trx_id', 'trx_ref', 'trx_msg']



class FollowerSerializer(serializers.ModelSerializer):
	follower = UserSerializer(read_only=True)
	created = serializers.DateTimeField(read_only=True, source='date_followed')
	class Meta:
		model = Follow
		fields = ['follower', 'created']



class CategorySerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(required=False)
	class Meta:
		model = Category
		fields = ['id', 'name', 'slug']
		lookup_field = 'slug'
		extra_kwargs = {
            'name': {
                'validators': [],
            },
            'id': {
            	'read_only': False,
            	'required': False
            }
        }
    	


class UpdateImagesSerializers(serializers.ModelSerializer):
	image = serializers.ImageField(max_length=None)
	class Meta:
		model = UpdateImage
		fields = ['image', 'date']



class ProjectUpdatesSerializer(serializers.ModelSerializer):
	title = serializers.CharField()
	image = serializers.SerializerMethodField()
	date = serializers.DateField(source="published")
	class Meta:
		model = Update
		fields = ['id', 'title', 'details', 'date', 'image']

	def get_image(self, obj):
		request = self.context.get('request')
		return request.build_absolute_uri(obj.get_image())

	def update(self, instance, validated_data):
		instance.title = validated_data.get('title', instance.title)
		instance.details = validated_data.get('details', instance.details)
		instance.image = validated_data.get('image', None)
		instance.save()
		return instance



class ProjectSerializer(serializers.ModelSerializer):
	author = UserSerializer(read_only=True)
	# image = serializers.ImageField(max_length=None, required=False)
	image =serializers.SerializerMethodField()
	category = CategorySerializer(read_only=False)
	created = serializers.DateField(source="published_date", read_only=True)
	donations = DonationSerializer(many=True, read_only=True)
	percent_raised = serializers.IntegerField(default=0)
	updates = ProjectUpdatesSerializer(many=True, read_only=True)
	total_donations = serializers.DecimalField(max_digits=9, decimal_places=2, read_only=True)
	expiry = serializers.DateTimeField(source="expiry_date", read_only=False)
	to_expire = serializers.IntegerField(read_only=True)
	followers = FollowerSerializer(many=True, read_only=True)
	slug = serializers.CharField(read_only=True)
	# is_featured = serializers.BooleanField()
	# paid = serializers.BooleanField()
	
	class Meta:
		model = Project
		fields = ['id', 'author', 'title', 'slug', 'details', 'goal', 'beneficiary', 'expiry', 'category', 'view_count', 'created',
		'donations', 'updates', 'total_donations', 'paid', 'image', 'percent_raised', 'to_expire', 'status', 'followers', 'slug', 'image', 'is_featured', 'can_update_expiry']
		
	def get_image(self, obj):
		request = self.context.get('request')
		return request.build_absolute_uri(obj.get_image())

	def create(self, validated_data):
		title = validated_data.get('title')
		details = validated_data.get('details')
		goal = validated_data.get('goal')
		exp = validated_data.get('expiry')
		expiry = datetime.strptime(str(exp), '%Y-%m-%d %H:%M:%S')
		
		beneficiary = validated_data.get('beneficiary')
		slug = slugify(title)
		image = validated_data.get('image', None)
		category_data = validated_data.pop('category')
		cat_id = category_data.get('id')
		if cat_id:
			category = Category.objects.get(id=cat_id)

		project = Project.objects.create(title=title, details=details, goal=goal, expiry=expiry, old_expiry=expiry,
                                         beneficiary=beneficiary, category=category, slug=slug, paid=False,
                                         image=image, author=self.context['request'].user)

		# send email
		context = {
			'project': project,
			'user': self.context['request'].user
		}
		html_content = render_to_string('projects/project_submitted.html', context)
		subject = 'Your project has been submitted for review'
		message = 'We are currently reviewing your project.'
		from_email = settings.EMAIL_HOST_USER
		email = self.context['request'].user.email
		to_email = email
		msg = EmailMultiAlternatives(subject, message, from_email,
                                     to=[to_email, from_email])
		msg.attach_alternative(html_content, "text/html")
		msg.send()

		return project



class ProfileImageSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(max_length=None)
    class Meta:
        model = get_user_model()
        fields = ['picture']

    def update(self, instance, validated_data):
        instance.picture = validated_data.get('picture', instance.picture)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['password']



class DisableAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['is_active']



class MyDonationsSerializer(serializers.ModelSerializer):
	project = ProjectSerializer(read_only=True)
	name = UserSerializer(read_only=True)
	amount = serializers.DecimalField(max_digits=9, decimal_places=2)
	date = serializers.DateTimeField(source="date_donated", read_only=True)

	class Meta:
		model = Donation
		fields = ['project', 'name', 'amount', 'comment', 'date']

	


class MyFollowsSerializers(serializers.ModelSerializer):
	project = ProjectSerializer(read_only=True)
	follower = UserSerializer(read_only=True)
	created = serializers.DateTimeField(read_only=True, source='date_followed')

	class Meta:
		model = Donation
		fields = ['project', 'follower', 'created']



class DonateSerializer(serializers.ModelSerializer):
	project = ProjectSerializer(read_only=True)
	name = UserSerializer(read_only=True)
	amount = serializers.DecimalField(max_digits=9, decimal_places=2)
	date = serializers.DateTimeField(source="date_donated", read_only=True)
	show_name = serializers.BooleanField()
	trx_id = serializers.IntegerField()
	trx_ref = serializers.CharField()
	trx_msg = serializers.CharField()

	class Meta:
		model = Donation
		fields = ['project', 'name', 'amount', 'comment', 'date', 'show_name', 'trx_id', 'trx_ref', 'trx_msg']

	def create(self, validated_data):
		amount = validated_data.get('amount')
		comment = validated_data.get('comment')
		show_name = validated_data.get('show_name')
		trx_id = validated_data.get('trx_id')
		trx_ref = validated_data.get('trx_ref')
		trx_msg = validated_data.get('trx_msg')
		name = self.context['request'].user
		project_id = self.context['project']
		project = Project.objects.get(id=project_id)

		donation = Donation.objects.create(amount=amount, show_name=show_name, comment=comment, trx_id=trx_id, trx_ref=trx_ref, trx_msg=trx_msg, name=name, project=project)
		
		# send email to receiver
		context = {
			'donation': donation,
			'project': donation.project,
			'user': self.context['request'].user
		}
		
		html_content = render_to_string('projects/donation_sent.html', context)
		subject = 'Your Project has received a donation'
		message = 'Your Project has received a donation.'
		from_email = settings.EMAIL_HOST_USER
		email = donation.project.author.email
		to_email = email
		msg = EmailMultiAlternatives(subject, message, from_email,
                                     to=[to_email, from_email])
		msg.attach_alternative(html_content, "text/html")
		msg.send()

		# send email to donor
		html_content = render_to_string('projects/thanks_for_donating.html', context)
		subject = 'Your donation has been received.'
		message = 'Your donation has been received and well appreciated.'
		email = self.context['request'].user.email
		to_email = email
		msg = EmailMultiAlternatives(subject, message, from_email, to=[to_email, from_email])
		msg.attach_alternative(html_content, "text/html")
		msg.send()

		return donation


class ProjectImageUploadSerializer(serializers.ModelSerializer):
	image = serializers.ImageField(max_length=None)

	class Meta:
		model = Project
		fields = ['image']

	def update(self, instance, validated_data):
		instance.image = validated_data.get('image', instance.image)
		instance.save()
		return instance


class BankDetailSerializer(serializers.ModelSerializer):
	user = UserSerializer(read_only=True)
	id_card = serializers.ImageField(max_length=None)

	class Meta:
		model = BankDetail
		fields = ['user', 'bank', 'account_type', 'account_number', 'account_name', 'id_card', 'created']

	def create(self, validated_data):
		bank = validated_data.get('bank')
		account_type = validated_data.get('account_type')
		account_number = validated_data.get('account_number')
		account_name = validated_data.get('account_name')
		id_card = validated_data.get('id_card', None)

		detail = BankDetail.objects.create(bank=bank, account_type=account_type, account_number=account_number, account_name=account_name, id_card=id_card, user=self.context['request'].user)
		# send email to receiver
		# send email to or
		return detail

	def update(self, instance, validated_data):
		instance.bank = validated_data.get('bank', instance.bank)
		instance.account_type = validated_data.get('account_type', instance.account_type)
		instance.account_number = validated_data.get('account_number', instance.account_number)
		instance.account_name = validated_data.get('account_name', instance.account_name)
		instance.save()
		return instance



class BankSerializer(serializers.ModelSerializer):
	class Meta:
		model = Bank
		fields = ['name', 'short_name']



class UserRegistrationSerializer(serializers.ModelSerializer):
    c_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    email = serializers.EmailField()
    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'email', 'gender', 'phone_no', 'location', 'password', 'c_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, email):
        queryset = get_user_model().objects.filter(email=email)
        if queryset:
            raise serializers.ValidationError("A user with that email address already exists. ")
        return email

    def save(self):
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        gender = self.validated_data['gender']
        phone_no = self.validated_data['phone_no']
        location = self.validated_data['location']
        password = self.validated_data['password']
        c_password = self.validated_data['c_password']

        if len(password) < 6 or len(password) > 20:
            raise serializers.ValidationError({'password': 'Password must be between 6 and 20 characters.'})

        if password != c_password:
            raise serializers.ValidationError({'password': 'Password and confirm password must match!'})

        # user = CustomUser(first_name=first_name, last_name=last_name, email=email, gender=gender, phone_no=phone_no, location=location)
        user = CustomUser.objects.create(first_name=first_name, last_name=last_name, email=email, gender=gender, phone_no=phone_no, location=location)
        user.set_password(password)
        user.save()

        # //send welcome mail
        context = {
            'data': user,
        }
        html_content = render_to_string('projects/welcome.html', context)
        subject = 'Welcome to Junkies'
        message = 'Welcome to Junkies'
        from_email = settings.EMAIL_HOST_USER
        to_email = email
        msg = EmailMultiAlternatives(subject, message, from_email,
                                     to=[to_email, from_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        Token.objects.create(user=user)



class CreateFollowerSerializer(serializers.ModelSerializer):
	project = ProjectSerializer(read_only=True)
	follower = UserSerializer(read_only=True)
	created = serializers.DateTimeField(source='date_followed', read_only=True)

	class Meta:
		model = Follow
		fields = ['project', 'follower', 'created']

	def create(self, validated_data):
		proj = self.context['project']
		project = Project.objects.get(id=proj)
		user = self.context['request'].user
		follow = Follow.objects.create(project=project, follower=user)
		return follow



class PasswordRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField
    class Meta:
        model = PasswordReset
        fields = ['email', 'token', 'created']

    def create(self, validated_data):
        email = validated_data.get('email')
        # remove any previous entry for this user from PasswordReset
        old_entry = PasswordReset.objects.get(email=email)
        old_entry.delete()

        user = get_user_model().objects.get(email=email)
        if user:
            # token = uuid.uuid4()
            token = secrets.token_hex(88)
            expiry = datetime.now() + timedelta(hours=1)
            entry = PasswordReset.objects.create(email=email, token=token, expiry=expiry)
            # send email
            frontend = 'http://localhost:8000/password_reset/{}/{}'.format(email, token)
            context = {
                'user': user.first_name,
                'email': email,
                'token': token,
                'frontend': frontend
            }
            subject = 'Password Reset Request On junkies.com'
            message = 'Password reset on junkies.com'
            to_email = user.email
            html_content = render_to_string('projects/password_reset_enquiry.html', context)
            msg = EmailMultiAlternatives(subject, message, from_email=settings.EMAIL_HOST_USER,
                                             to=[to_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return entry
        raise serializers.ValidationError("User with that email doesn't exist in our database.")



class ResetUserPasswordSerializer(serializers.ModelSerializer):
    c_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'c_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        token = self.validated_data['token']
        req = PasswordReset.objects.get(token=token)
        email = req.email
        user = get_user_model().objects.get(email=email)

        password = self.validated_data['password']
        c_password = self.validated_data['c_password']

        if len(password) < 6 or len(password) > 20:
            raise serializers.ValidationError({'password': 'Password must be between 6 and 20 characters.'})

        if password != c_password:
            raise serializers.ValidationError({'password': 'Password and confirm password must match!'})
            user.set_password(password)
            user.save()
            return user



class PasswordResetSerializer(serializers.ModelSerializer):
	class Meta:
		model = get_user_model()
		fields = ['password']
		extra_kwargs = {
			'password': {'write_only': True}
		}

	def save(self, **kwargs):
		token = self.validated_data['token']
		req = PasswordReset.objects.get(token=token)
		email = req.email
		user = get_user_model().objects.get(email=email)

		password = self.validated_data['password']
		c_password = self.validated_data['c_password']

		if len(password) < 6 or len(password) > 20:
			raise serializers.ValidationError({'password': 'Password must be between 6 and 20 characters.'})
		
		if password != c_password:
			raise serializers.ValidationError({'password': 'Password and confirm password must match!'})

		user.set_password(password)
		user.save()

		# send email to notify user
		context = {
			'user': instance.first_name
		}

		subject = 'Your password has been reset!'
		message = 'Password reset successfully!'
		to_email = email
		html_content = render_to_string('projects/password_reset_success.html', context)
		msg = EmailMultiAlternatives(subject, message, from_email=settings.EMAIL_HOST_USER, to=[to_email])
		msg.attach_alternative(html_content, "text/html")
		msg.send()

		return user



class SuccessStorySerializer(serializers.ModelSerializer):
	project = ProjectSerializer(read_only=True)
	date = serializers.DateTimeField(read_only=True)
	class Meta:
		model = SuccessStory
		fields = ['id', 'project', 'title', 'details', 'is_approved', 'is_featured', 'date']

	def update(self, instance, validated_data):
		instance.title = validated_data.get('title')
		instance.details = validated_data.get('details')
		instance.save()
		return instance

	def create(self, validated_data):
		proj = self.context['project']
		project = Project.objects.get(id=proj)
		title = validated_data.get('title')
		details = validated_data.get('details')
		story = SuccessStory.objects.create(project=project, title=title, details=details)
		return story



class UpdateProjectSerializer(serializers.ModelSerializer):
	title = serializers.CharField()
	details = serializers.CharField()
	image = serializers.ImageField(max_length=None)

	class Meta:
		model = Project
		fields = ['title', 'details', 'image', 'slug']

	def update(self, instance, validated_data):
		instance.title = validated_data.get('title', instance.title)
		instance.details = validated_data.get('details', instance.details)
		instance.slug = slugify(validated_data.get('title', instance.title))
		# img = validated_data.get('image')
		# if img:
		# 	instance.image.delete()
		# 	instance.image = img
		instance.save()
		return instance



class UpdateProjectExpirySerializer(serializers.ModelSerializer):
	expiry = serializers.DateTimeField()
	old_expiry = serializers.DateTimeField()
	can_update_expiry = serializers.BooleanField()
	class Meta:
		model = Project
		fields = ['expiry', 'old_expiry', 'can_update_expiry']

	def update(self, instance, validated_data):
		instance.old_expiry = instance.expiry
		instance.expiry = validated_data.get('expiry', instance.expiry)
		instance.can_update_expiry = False
		instance.save()
		return instance


class CreateProjectUpdateSerializer(serializers.ModelSerializer):
	project = ProjectSerializer(read_only=True)
	title = serializers.CharField()
	details = serializers.CharField()
	date = serializers.DateTimeField(source="published", read_only=True)
	image = serializers.SerializerMethodField()

	class Meta:
		model = Update
		fields = ['id', 'project', 'title', 'details', 'date', 'image']

	def get_image(self, obj):
		request = self.context.get('request')
		return request.build_absolute_uri(obj.get_image())
		
	def create(self, validated_data):
		title = validated_data.get('title')
		details = validated_data.get('details')
		image = validated_data.get('image', None)
		project_id = self.context['project']
		project = Project.objects.get(id=project_id)
		update = Update.objects.create(title=title, details=details, project=project, image=image)
		return update


class UpdateImageUploadSerializer(serializers.ModelSerializer):
	image = serializers.ImageField(max_length=None)
	project = ProjectSerializer(read_only=True)
	title = serializers.CharField()
	details = serializers.CharField()
	date = serializers.DateTimeField(source="published", read_only=True)

	class Meta:
		model = Update
		fields = ['id', 'project', 'title', 'details', 'date', 'image']

	def update(self, instance, validated_data):
		instance.image = validated_data.get('image', instance.image)
		instance.save()
		return instance



class EnquiryContactSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = EnquiryContact
        fields = ['email', 'f_name', 'l_name', 'phone', 'subject', 'message']

    def create(self, validated_data):
        from_email = validated_data.get('email')
        f_name = validated_data.get('f_name')
        l_name = validated_data.get('l_name')
        phone = validated_data.get('phone')
        subject = 'Enquiry: ' + validated_data.get('subject')
        message = validated_data.get('message')
        application = super(EnquiryContactSerializer, self).create(validated_data)
        to_email = 'vidspectra20@gmail.com'
        app = EnquiryContact(**validated_data)
        context = {
            'data': app,
        }
        html_content = render_to_string('projects/enquiry.html', context)

        # //send message to kolabo
        msg = EmailMultiAlternatives(subject, message, from_email,
                                     to=[to_email, settings.EMAIL_HOST_USER])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # send acknowledgement to sender
        subject2 = 'Enquiry: Re- ' + validated_data.get('subject')
        message2 = 'Your enquiry has been sent to kolabo.com. We shall get back to you shortly. Thank You.'
        from_email2 = settings.EMAIL_HOST_USER
        enq = validated_data.get('email')
        html_content2 = render_to_string('projects/enquiry_ackn.html', context)
        mgs = EmailMultiAlternatives(subject2, message2, from_email2, to=[enq])
        msg.attach_alternative(html_content2, "text/html")
        msg.send()
        return application



class MemberSerializer(serializers.ModelSerializer):
	fullname = serializers.CharField(source="get_fullname")
	class Meta:
		model = get_user_model()
		fields = ['id', 'first_name', 'last_name', 'fullname', 'email', 'phone_no', 'location', 'picture']



class MyProjectSerializer(serializers.ModelSerializer):
	author = UserSerializer(read_only=True)
	category = CategorySerializer(read_only=False)
	created = serializers.DateField(source="published_date", read_only=True)
	donations = DonationSerializer(many=True, read_only=True)
	percent_raised = serializers.IntegerField(default=0)
	updates = ProjectUpdatesSerializer(many=True, read_only=True)
	total_donations = serializers.DecimalField(max_digits=9, decimal_places=2, read_only=True)
	expiry = serializers.DateTimeField(source="expiry_date", read_only=False)
	to_expire = serializers.IntegerField(read_only=True)
	followers = FollowerSerializer(many=True, read_only=True)
	slug = serializers.CharField(read_only=True)
	
	class Meta:
		model = Project
		fields = ['id', 'author', 'title', 'slug', 'details', 'goal', 'beneficiary', 'expiry', 'category', 'view_count', 'created',
		'donations', 'updates', 'total_donations', 'paid', 'percent_raised', 'to_expire', 'status', 'followers', 'slug']



class WithdrawRequestSerializer(serializers.ModelSerializer):
	user = UserSerializer(read_only=True)
	project = ProjectSerializer(read_only=True)
	created = serializers.DateField(source="date", read_only=True)
    
	class Meta:
		model = WithdrawRequest
		fields = ['user', 'project', 'amount', 'is_approved', 'created']

	def create(self, validated_data):
		proj = self.context['project']
		project = Project.objects.get(id=proj)
		amount = validated_data.get('amount')
		user = self.context['request'].user
		req = WithdrawRequest.objects.create(project=project, amount=amount, user=user)

		# send email to user
		context = {
            'req': req,
        }
		subject = 'Request for fund withdrawal on Kolabo'
		admin = 'banklan2010@gmail.com'
		from_email = settings.EMAIL_HOST_USER
		message = 'We have received your request for fund withdraw for your campaign.'
		to = project.author.email
		html_content = render_to_string('projects/request_for_withdrawal.html', context)
		msg = EmailMultiAlternatives(subject, message, from_email, to=[to, admin])
		msg.attach_alternative(html_content, "text/html")
		msg.send()

		return req





