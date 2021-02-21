from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.utils import timezone
from django.utils.text import slugify
from datetime import datetime
from django.template.loader import render_to_string
from rest_framework import viewsets, status, serializers
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (
	UserSerializer, CategorySerializer, ProjectSerializer, DonationSerializer, ProjectUpdatesSerializer,
	ProfileImageSerializer, ChangePasswordSerializer, DisableAccountSerializer, MyDonationsSerializer, 
	MyFollowsSerializers, DonateSerializer, ProjectImageUploadSerializer, BankDetailSerializer, BankSerializer,
    UserRegistrationSerializer, FollowerSerializer, CreateFollowerSerializer, PasswordRequestSerializer,
    PasswordRequestSerializer, ResetUserPasswordSerializer, PasswordResetSerializer, SuccessStorySerializer,
    UpdateProjectSerializer, UpdateProjectExpirySerializer, CreateProjectUpdateSerializer, UpdateImageUploadSerializer,
    EnquiryContactSerializer, MemberSerializer, MyProjectSerializer, WithdrawRequestSerializer
)
from .models import (
    Category, Project, Donation, Update, UpdateImage, ProjectReport, Follow, BankDetail, Bank, PasswordReset,
    SuccessStory, EnquiryContact, WithdrawRequest
)
from .pagination import ProjectListPagination


class UserViewSets(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny,]
    authentication_classes = [TokenAuthentication, ]


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = get_user_model().objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'status': 'success',
            'message': 'Your registration was successful. Thank you.',
            'resp': status.HTTP_201_CREATED,
            'user': serializer.data
        }
        return Response(response)



class RetrieveProfileViewSet(RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def retrieve(self, request, *args, **kwargs):
        user = request.user.id
        queryset = self.get_queryset().get(id=user)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)


class UpdateProfileViewSet(UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get_object(self):
        profile = get_user_model().objects.get(id=self.request.user.id)
        return profile

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)



class UpdateProfilePictureViewSet(UpdateAPIView):
	queryset = get_user_model().objects.all()
	serializer_class = ProfileImageSerializer
	permission_classes = [IsAuthenticated,]
	authentication_classes = [TokenAuthentication,]

	def get_object(self):
		user = self.request.user.id
		profile = get_user_model().objects.get(id=user)
		return profile

	def update(self, request, *args, **kwargs):
		instance = self.get_object()
		# context = {
  #           'request': request
  #       }
		if instance.picture is None:
			serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
			serializer.is_valid(raise_exception=True)
			self.perform_update(serializer)
			return Response(serializer.data)
		else:
			instance.picture.delete()
			serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
			serializer.is_valid(raise_exception=True)
			self.perform_update(serializer)
			return Response(serializer.data)



class CategoryViewSets(viewsets.ModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer


class CategoryBySlugViewSet(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def retrieve(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        queryset = self.get_queryset().get(slug=slug)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)



class ProjectViewSets(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = ProjectListPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    # filterset_fields = ('state__slug', 'subcategory__category__slug')
    # search_fields = ['title', 'details', 'beneficiary', 'author__first_name', 'author__last_name']

    def get_object(self):
        item = super(ProjectViewSets, self).get_object()
        item.incrementViewCount()
        return item


class RelatedProjectsViewSets(ListAPIView):
	serializer_class = ProjectSerializer

	def list(self, request, *args, **kwargs):
		proj = kwargs.get('proj')
		queryset = Project.objects.filter(category__id=proj)
		serializer = self.serializer_class(queryset, many=True, context={"request": request})
		return Response(serializer.data)


class DonationViewSets(ListAPIView):
	serializer_class = DonationSerializer

	def list(self, request, *args, **kwargs):
		proj = kwargs.get('project')
		queryset = Donation.objects.filter(project_id = proj)
		serializer = self.serializer_class(queryset, many=True, context={"request": request})
		return Response(serializer.data)



class UpdatePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get_object(self):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # check old password
            if not instance.check_password(serializer.data.get('password')):
                return Response({'status': 'failed', 'message': 'Invalid Password'}, status=status.HTTP_400_BAD_REQUEST)

            if request.data.get('confirm_password') != request.data.get('new_password'):
                raise serializer.ValidationError({'password': 'New password and Confirm password must match'})

            # if everything is ok
            instance.set_password(request.data.get('new_password'))
            instance.save()
            update_session_auth_hash(request, instance)
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully'
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DisableAccountViewSet(UpdateAPIView):
    serializer_class = DisableAccountSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get_object(self):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance.is_active = False
        serializer.save()
        return Response(serializer.data)



class MyProjectsViewSet(ListAPIView):
	serializer_class = ProjectSerializer
	permission_classes = [IsAuthenticated, ]
	authentication_classes = [TokenAuthentication, ]

	def list(self, request, *args, **kwargs):
		me = self.request.user.id
		queryset = Project.objects.filter(author__id = me)
		serializer = self.serializer_class(queryset, many=True, context={"request": request})
		return Response(serializer.data)



class UpdateMyProjectViewSet(UpdateAPIView):
    serializer_class = UpdateProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication, ]

    def get_object(self):
        id = self.kwargs.get('pk')
        obj = self.get_queryset().get(id=id, author=self.request.user)
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(slug=slugify(request.data['title']))
        return Response(serializer.data)


class UpdateMyProjectExpiry(UpdateAPIView):
    serializer_class = UpdateProjectExpirySerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication, ]

    def get_object(self):
        id = self.kwargs.get('pk')
        obj = self.get_queryset().get(id=id, author=self.request.user)
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



class MyDonationsViewSets(ListAPIView):
	serializer_class = MyDonationsSerializer
	permission_classes = [IsAuthenticated,]
	authentication_classes = [TokenAuthentication, ]

	def list(self, request, *args, **kwargs):
		me = self.request.user.id
		queryset = Donation.objects.filter(name__id = me)
		serializer = self.serializer_class(queryset, many=True, context={"request": request})
		return Response(serializer.data)


class MyFollowsViewSets(ListAPIView):
	serializer_class = MyFollowsSerializers
	permission_classes = [IsAuthenticated,]
	authentication_classes = [TokenAuthentication, ]

	def list(self, request, *args, **kwargs):
		me = self.request.user.id
		queryset = Follow.objects.filter(follower__id=me)
		serializer = self.serializer_class(queryset, many=True, context={"request": request})
		return Response(serializer.data)


class DonationCreateViewSet(CreateAPIView):
    serializer_class = DonateSerializer
    queryset = Donation.objects.all()
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get_serializer_context(self):
        return{"project": self.kwargs['project'], "request": self.request}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project_id = kwargs.get('project')
        project = Project.objects.get(id=project_id)
        serializer.save(project=project, date=timezone.now)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CreateProjectViewSet(CreateAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def create(self, request, *args, **kwargs):
        context = {
            'request': request
        }
        # print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response = {'message': 'Project created!', 'result': serializer.data}
        return Response(response, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(created=timezone.now(), expiry=self.request.data['expiry'])


class CreateProjectImageViewSet(UpdateAPIView):
    serializer_class = ProjectImageUploadSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get_object(self):
        id = self.kwargs.get('pk')
        project = self.get_queryset().get(id=id)
        return project

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.image is not None:
            instance.image.delete()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LinkedAccountViewSet(RetrieveAPIView):
    serializer_class = BankDetailSerializer
    queryset = BankDetail.objects.all()
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        try:
            queryset = self.get_queryset().get(user=user)
            serializer = self.get_serializer(queryset)
            return Response(serializer.data)

        except ObjectDoesNotExist:
            res = {
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'There is no linked account for this user',
            }
            return Response(res)



class CreateBankDetailsViewSet(CreateAPIView):
    serializer_class = BankDetailSerializer
    queryset = BankDetail.objects.all()
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get_serializer_context(self):
        return{"request": self.request}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        serializer.save(user=user, created=timezone.now)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class UpdateBankDetailsViewSet(UpdateAPIView):
    serializer_class = BankDetailSerializer
    queryset = BankDetail.objects.all()
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get_object(self):
        user = self.request.user
        detail = BankDetail.objects.get(user=user)
        return detail

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance.is_active = False
        serializer.save()
        return Response(serializer.data)



class BankViewSet(viewsets.ModelViewSet):
    serializer_class = BankSerializer
    queryset = Bank.objects.all()
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]



class UploadProfilePictureViewSet(UpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ProfileImageSerializer

    def get_object(self):
        user_email = self.request.data['new_user']
        profile = get_user_model().objects.get(email=user_email)
        return profile

    def update(self, request, *args, **kwargs):
        print(request.data)
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)



class CreateFollowViewSet(CreateAPIView):
    serializer_class = CreateFollowerSerializer
    queryset = Follow.objects.all()
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get_serializer_context(self):
        return{"project": self.kwargs['project'], "request": self.request}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        # user = self.request.user
        # proj = self.kwargs['project']
        # project = Project.objects.get(id=proj)
        # self.perform_create(serializer)
        serializer.save(date=timezone.now)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class RequestPasswordReset(CreateAPIView):
    queryset = PasswordReset.objects.all()
    serializer_class = PasswordRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {'message': 'Password request mail Sent!', 'result': serializer.data}
        headers = self.get_success_headers(serializer.data)
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)


class VerifyTokenViewSet(RetrieveAPIView):
    queryset = PasswordReset.objects.all()
    serializer_class = PasswordRequestSerializer

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_queryset().get(token=kwargs.get('token'), email=kwargs.get('email'))
        if obj:
            if obj.expiry > datetime.now():
                serializer = self.get_serializer(obj)
                response = {'message': 'ok', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)

            res = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Token has expired',
            }
            return Response(res)
        res = {
            'status': status.HTTP_404_NOT_FOUND,
            'message': 'User does not exist on our database',
        }
        return Response(res)



class ResetPasswordView(UpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = PasswordResetSerializer

    def get_object(self):
        token = self.request.data['token']
        req = PasswordReset.objects.get(token=token)
        obj = self.get_queryset().get(email=req.email)
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            # if everything is ok
            new_pswd = self.request.data['password']
            instance.set_password(new_pswd)
            instance.save()
            update_session_auth_hash(request, instance)

            # delete the password reset entry from db
            token = self.request.data['token']
            req = PasswordReset.objects.get(token=token)
            req.delete()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password reset successfully'
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SuccessStoryViewSets(viewsets.ModelViewSet):
    queryset = SuccessStory.objects.all()
    serializer_class = SuccessStorySerializer



class ListProjectsByCat(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = ProjectListPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    # filterset_fields = ('category__slug')
    search_fields = ['title', 'beneficiary', 'details', 'goal', 'author__first_name', 'author__last_name']

    def get_queryset(self):
        queryset = Project.objects.filter(category__slug=self.kwargs.get('slug'))
        return queryset


class SearchProjectsViewSet(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # pagination_class = ProjectListPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    # filterset_fields = ('state__slug', 'subcategory__category__slug')
    search_fields = ['title', 'details', 'beneficiary', 'author__first_name', 'author__last_name']


class ProjectListViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class CampaignDeleteViewSet(DestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get_object(self):
        proj = self.kwargs.get('proj')
        project = self.get_queryset().filter(id=proj, author=self.request.user)
        return project

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateDestroyViewSet(DestroyAPIView):
    queryset = Update.objects.all()
    serializer_class = ProjectUpdatesSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get_object(self):
        id = self.kwargs.get('updt')
        update = self.get_queryset().get(id=id)
        return update

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ModifyProjectUpdates(UpdateAPIView):
    queryset = Update.objects.all()
    serializer_class = ProjectUpdatesSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get_object(self):
        id = self.kwargs.get('updt')
        update = self.get_queryset().get(id=id)
        return update

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'image' in request.data:
            instance.image.delete()
            image = request.data['image']
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(image=image)
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)


class AddProjectUpdate(CreateAPIView):
    queryset = Update.objects.all()
    serializer_class = CreateProjectUpdateSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get_serializer_context(self):
        return{"project": self.kwargs['project'], "request": self.request}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(date=timezone.now)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class AddUpdateImageViewSet(UpdateAPIView):
    queryset = Update.objects.all()
    serializer_class = UpdateImageUploadSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get_object(self):
        id = self.kwargs.get('updt')
        update = self.get_queryset().get(id=id)
        return update

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.image is not None:
            instance.image.delete()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



class ProjectSuccessStoryViewSet(RetrieveAPIView):
    queryset = SuccessStory.objects.all()
    serializer_class = SuccessStorySerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def retrieve(self, request, *args, **kwargs):
        proj = self.kwargs['proj']
        try:
            queryset = self.get_queryset().get(project__id=proj)
            serializer = self.get_serializer(queryset)
            return Response(serializer.data)

        except ObjectDoesNotExist:
            res = {
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'There is no success story for this campaign.',
            }
            return Response(res)



class StoryUpdateViewSet(UpdateAPIView):
    queryset = SuccessStory.objects.all()
    serializer_class = SuccessStorySerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get_object(self):
        id = self.kwargs.get('story')
        obj = self.get_queryset().get(id=id)
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



class StoryDeleteViewSet(DestroyAPIView):
    queryset = SuccessStory.objects.all()
    serializer_class = SuccessStorySerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get_object(self):
        id = self.kwargs.get('story')
        obj = self.get_queryset().get(id=id)
        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class AddStoryViewSet(CreateAPIView):
    queryset = SuccessStory.objects.all()
    serializer_class = SuccessStorySerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def get_serializer_context(self):
        return{"project": self.kwargs['project'], "request": self.request}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created=timezone.now)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class FeaturedStoriesViewSet(ListAPIView):
    queryset = SuccessStory.objects.all()
    serializer_class = SuccessStorySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(is_featured=True)
        serializer = self.serializer_class(queryset, many=True, context={"request": request})
        return Response(serializer.data)



class EnquiryContactViewSet(CreateAPIView):
    serializer_class = EnquiryContactSerializer
    queryset = EnquiryContact.objects.all()

    # @csrf_exempt
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {'message': 'Enquiry Sent!', 'result': serializer.data}
        headers = self.get_success_headers(serializer.data)
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)



class MemberProfileViewSet(RetrieveAPIView):
    serializer_class = MemberSerializer
    queryset = get_user_model().objects.all()

    def retrieve(self, request, *args, **kwargs):
        user = kwargs.get('pk')
        queryset = self.get_queryset().get(id=user)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)



class UserCampaignsViewSet(ListAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def list(self, request, *args, **kwargs):
        user = kwargs.get('user')
        queryset = Project.objects.filter(author__id=user)
        serializer = self.serializer_class(queryset, many=True, context={"request": request})
        return Response(serializer.data)



class ProjectBySlugViewSet(RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = MyProjectSerializer

    def retrieve(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        queryset = self.get_queryset().get(slug=slug)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)


class WithdrawalRequestViewSet(CreateAPIView):
    serializer_class = WithdrawRequestSerializer
    queryset = WithdrawRequest.objects.all()
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get_serializer_context(self):
        return{"project": self.kwargs['project'], "request": self.request}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project_id = kwargs.get('project')
        project = Project.objects.get(id=project_id)
        serializer.save(project=project, created=timezone.now)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CheckWithdrawRequestViewSet(RetrieveAPIView):
    queryset = WithdrawRequest.objects.all()
    serializer_class = WithdrawRequestSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def retrieve(self, request, *args, **kwargs):
        proj = self.kwargs['proj']
        try:
            queryset = self.get_queryset().get(project__id=proj)
            serializer = self.get_serializer(queryset)
            return Response(serializer.data)

        except ObjectDoesNotExist:
            res = {
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'There is no withdraw request for this campaign.',
            }
            return Response(res)





# class Popular
# class ProjectsListViewSet(viewsets.ModelViewSet):
    # queryset = Project.objects.all()
    # serializer_class = ProjectSerializer

    # def get_object(self):
    #     item = super(ProjectsListViewSet, self).get_object()
    #     item.incrementViewCount()
    #     return item






# class SendWelcomeEmail(CreateAPIView):
#     serializer_class = WelcomeMailSerializer
#     queryset = get_user_model().objects.all()

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         response = {
#             'status': 'success',
#             'message': 'Welcome mail has been sent successfully.',
#             'resp': status.HTTP_201_CREATED,
#         }
#         return Response(response)
       



    




