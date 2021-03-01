
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.authtoken import views
from projects.views import (
	UserViewSets, ProjectViewSets, RelatedProjectsViewSets, DonationViewSets, RetrieveProfileViewSet, UpdateProfileViewSet,
	UpdateProfilePictureViewSet, UpdatePasswordView, DisableAccountViewSet, MyProjectsViewSet, MyDonationsViewSets,
	MyFollowsViewSets, DonationCreateViewSet, CategoryViewSets, CreateProjectViewSet, CreateProjectImageViewSet,
	LinkedAccountViewSet, BankViewSet, CreateBankDetailsViewSet, UpdateBankDetailsViewSet, UserCreateAPIView,
	UploadProfilePictureViewSet, CreateFollowViewSet, RequestPasswordReset, VerifyTokenViewSet, ResetPasswordView,
	SuccessStoryViewSets, ListProjectsByCat, SearchProjectsViewSet, ProjectListViewSet, CampaignDeleteViewSet,
	UpdateMyProjectViewSet, UpdateMyProjectExpiry, UpdateDestroyViewSet, ModifyProjectUpdates, AddProjectUpdate,
	AddUpdateImageViewSet, ProjectSuccessStoryViewSet, StoryUpdateViewSet, StoryDeleteViewSet, AddStoryViewSet,
	FeaturedStoriesViewSet, CategoryBySlugViewSet, EnquiryContactViewSet, MemberProfileViewSet, UserCampaignsViewSet,
	ProjectBySlugViewSet, WithdrawalRequestViewSet, CheckWithdrawRequestViewSet
)

router = routers.DefaultRouter()
router.register('users', UserViewSets, basename='users')
router.register('projects', ProjectViewSets, basename='campaigns')
router.register('categories', CategoryViewSets, basename="categories")
router.register('banks', BankViewSet, basename="banks")
router.register('success_stories', SuccessStoryViewSets, basename="success-story")
router.register('project_list', ProjectListViewSet, basename="project-list")
# router.register('backers',  DonationViewSets, basename='backers')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="index.html"),name="app"),
    path('campaigns/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('campaign/<int:pk>/<slug:slug>/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('campaign_backers/<int:id>/<slug:slug>/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('login/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('register/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('register/upload_profile_photo/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('profile/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('my-campaign/<int:id>/<slug:slug>/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('back_campaign/<int:id>/<slug:slug>/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('checkout/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('checkedout_successful/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('create_new/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('create_new2/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('create_new3/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('review_new_campaign/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('create_new_add_image/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('profile/bank_details/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('forgot_password/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('password_reset/<str:email>/<str:token>/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('password_reset_success/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('campaigns/<slug:slug>/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('search_result/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('popular_campaigns', TemplateView.as_view(template_name="index.html"), name="app"),
    path('manage_campaign/<int:proj>/<str:slug>/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('success_story/<int:pk>/<str:slug>/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('success_stories/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('how_it_works/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('about-us/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('faq/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('terms-conditions/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('privacy-policy/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('contact/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('members-page/<int:pk>/<str:slug>/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('request-withdrawal/<int:pk>/<str:slug>/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('request-withdrawal-successful/', TemplateView.as_view(template_name="index.html"), name="app"),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', views.obtain_auth_token, name="api-token-auth"),
    path('rest-auth/', include('rest_auth.urls')),
    path('api/profile/', RetrieveProfileViewSet.as_view(), name="get-profile"),
    path('api/profile/update/', UpdateProfileViewSet.as_view(), name="update-profile"),
    path('api/profile_image/update/', UpdateProfilePictureViewSet.as_view(), name="update-profile-pic"),
    path('api/profile_picture/upload/', UploadProfilePictureViewSet.as_view(), name="upload-profile-pic"),
    path('api/same_categ/<int:proj>/', RelatedProjectsViewSets.as_view(), name="related_projects"),
    path('api/campaign_backers/<int:project>/', DonationViewSets.as_view(), name="backers"),
    path('api/password-change/', UpdatePasswordView.as_view(), name="password-change"),
    path('api/disable-account/', DisableAccountViewSet.as_view(), name="disable-account"),
    path('api/my-projects/', MyProjectsViewSet.as_view(), name="my-projects"),
    path('api/update-my-project-details/<int:pk>/', UpdateMyProjectViewSet.as_view(), name="update-proj-details"),
    path('api/update-expiry-date/<int:pk>/', UpdateMyProjectExpiry.as_view(), name="update-proj-exp"),
    path('api/my-donations/', MyDonationsViewSets.as_view(), name="my-donations"),
    path('api/my-follows/', MyFollowsViewSets.as_view(), name="my-follows"),
    path('api/post-donation/<int:project>/', DonationCreateViewSet.as_view(), name="post-donation"),
    path('api/create-project/', CreateProjectViewSet.as_view(), name="create-project"),
    path('api/create-project-image/<int:pk>/', CreateProjectImageViewSet.as_view(), name="upload-image"),
    path('api/check-linked-account/', LinkedAccountViewSet.as_view(), name="check-account"),
    path('api/add-bank-details/', CreateBankDetailsViewSet.as_view(), name="add-details"),
    path('api/update-bank-details/', UpdateBankDetailsViewSet.as_view(), name="update-details"),
    path('api/user/register/', UserCreateAPIView.as_view(), name="register"),
    path('api/follow-campaign/<int:project>/', CreateFollowViewSet.as_view(), name="follow"),
    path('api/request_password_reset/', RequestPasswordReset.as_view(), name="request-pswd-reset"),
    path('api/verify_token/<str:email>/<str:token>/', VerifyTokenViewSet.as_view(), name="reset-confirm"),
    path('api/reset_password/', ResetPasswordView.as_view(), name="password-reset"),
    path('api/projects_by_cat/<slug:slug>/', ListProjectsByCat.as_view(), name="project-by-cat"),
    path('api/search_for_projects/', SearchProjectsViewSet.as_view(), name="search-for-projects"),
    path('api/delete_project/<int:proj>/', CampaignDeleteViewSet.as_view(), name="delete-my-project"),
    path('api/update_delete/<int:updt>/', UpdateDestroyViewSet.as_view(), name="delete-update"),
    path('api/modify_update/<int:updt>/', ModifyProjectUpdates.as_view(), name="modify-update"),
    path('api/add-update/<int:project>/', AddProjectUpdate.as_view(), name="create-update"),
    path('api/add-update-image/<int:updt>/', AddUpdateImageViewSet.as_view(), name="add-updateimg"),
    path('api/success_story/<int:proj>/', ProjectSuccessStoryViewSet.as_view(), name="success"),
    path('api/update_story/<int:story>/', StoryUpdateViewSet.as_view(), name="story-update"),
    path('api/delete_story/<int:story>/', StoryDeleteViewSet.as_view(), name="story-delete"),
    path('api/add_story/<int:project>/', AddStoryViewSet.as_view(), name="new-story"),
    path('api/featured_success_stories/', FeaturedStoriesViewSet.as_view(), name="featured-story"),
    path('api/get_cat_name/<slug:slug>/', CategoryBySlugViewSet.as_view(), name="get-categories"),
    path('api/send_enquiry/', EnquiryContactViewSet.as_view(), name="send-enquiry"),
    path('api/members_profile/<int:pk>/', MemberProfileViewSet.as_view(), name="member-profile"),
    path('api/user_campaigns/<int:user>/', UserCampaignsViewSet.as_view(), name="user-campaigns"),
    path('api/projects_by_slug/<str:slug>/', ProjectBySlugViewSet.as_view(), name="project-by-slug"),
    path('api/withdrawal_request/<int:project>/', WithdrawalRequestViewSet.as_view(), name="withdraw-request"),
    path('api/check_withdrawal_request/<int:proj>/', CheckWithdrawRequestViewSet.as_view(), name="check-withdraw-request")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
