import Home from './components/Home';
import Campaigns from './components/Campaigns';
import CampaignShow from './components/CampaignShow';
import CampaignBackers from './components/CampaignBackers';
import Login from './components/Login';
import Register from './components/Register';
import UploadProfilePhoto from './components/UploadProfilePhoto';
import MyProfile from './components/MyProfile';
import MyCampaign from './components/MyCampaign';
import MembersPage from './components/MembersPage';
import BackCampaign from './components/BackCampaign';
import Checkout from './components/Checkout';
import CheckedOutSuccess from './components/CheckedOutSuccess';
import CreateNew from './components/CreateNew';
import CreateNew2 from './components/CreateNew2';
import CreateNew3 from './components/CreateNew3';
import NewCampaignReview from './components/NewCampaignReview';
import CreateAddImage from './components/CreateAddImage';
import BankDetails from './components/BankDetails';
import RegisteredSuccessfully from './components/RegisteredSuccessfully';
import ForgotPassword from './components/ForgotPassword';
import PasswordReset from './components/PasswordReset';
import PasswordResetSuccess from './components/PasswordResetSuccess';
import CampaignsByCat from './components/CampaignsByCat';
import CampaignSearchResults from './components/CampaignSearchResults';
import TestRoute from './components/TestRoute';
import PopularCampaigns from './components/PopularCampaigns';
import ManageMyCampaign from './components/ManageMyCampaign';
import SuccessStoryShow from './components/SuccessStoryShow';
import SuccessStoriesList from './components/SuccessStoriesList';
import HowItWorks from './components/HowItWorks';
import AboutUs from './components/AboutUs';
import Faq from './components/Faq';
import TermsAndConditions from './components/TermsAndConditions';
import PrivacyPolicy from './components/PrivacyPolicy';
import FraudPolicy from './components/FraudPolicy';
import ContactUs from './components/Contact';
import RequestWithdrawal from './components/RequestWithdrawal';
import WithdrawReqSuccess from './components/WithdrawReqSuccess';


export default [
    {path: '/', name: 'Home', component: Home},
    { path: '/campaigns', name: 'Campaigns', component: Campaigns },
    { path: '/campaign/:id/:slug', name: 'CampaignShow', component: CampaignShow },
    { path: '/campaign_backers/:id/:slug', name: 'CampaignBackers', component: CampaignBackers },
    { path: '/login', name:'Login', component: Login},
    { path: '/register', name: 'Register', component: Register },
    { path: '/register/upload_profile_photo', name: 'UploadProfilePhoto', component: UploadProfilePhoto },
    { path: '/profile', name: 'MyProfile', component: MyProfile },
    { path: '/my-campaign/:id/:slug', name: 'MyCampaign', component: MyCampaign },
    { path: '/members-page/:id/:slug', name: 'MembersPage', component: MembersPage},
    { path: '/back_campaign/:id/:slug', name: 'BackCampaign', component: BackCampaign},
    { path: '/checkout', name: 'Checkout', component: Checkout},
    { path: '/checkedout_successful', name: 'CheckedOutSuccess', component: CheckedOutSuccess},
    { path: '/create_new', name: 'CreateNew', component: CreateNew},
    { path: '/create_new2', name: 'CreateNew2', component: CreateNew2},
    { path: '/create_new3', name: 'CreateNew3', component: CreateNew3},
    { path: '/review_new_campaign', name: 'NewCampaignReview', component: NewCampaignReview},
    { path: '/create_new_add_image', name: 'CreateAddImage', component: CreateAddImage},
    { path: '/profile/bank_details', name: 'BankDetails', component: BankDetails},
    { path: '/registered_successfully', name: 'RegisteredSuccessfully', component: RegisteredSuccessfully},
    { path: '/forgot_password', name: 'ForgotPassword', component: ForgotPassword },
    {path: '/password_reset/:email/:token', name: 'PasswordReset', component: PasswordReset},
    {path: '/password_reset_success', name: 'PasswordResetSuccess', component: PasswordResetSuccess},
    { path: '/campaigns/:slug', name: 'CampaignsByCat', component: CampaignsByCat },
    {path: '/search_result', name: 'CampaignSearchResults', component: CampaignSearchResults, props: true},
    {path: '/test', name: 'TestRoute', component: TestRoute, props: true},
    {path: '/popular_campaigns', name: 'PopularCampaigns', component: PopularCampaigns},
    { path: '/manage_campaign/:id/:slug', name: 'ManageMyCampaign', component: ManageMyCampaign},
    {path: '/success_story/:id/:slug', name: 'SuccessStoryShow', component: SuccessStoryShow},
    {path: '/success_stories', name: 'SuccessStoriesList', component: SuccessStoriesList},
    {path: '/how_it_works', name: 'HowItWorks', component: HowItWorks},
    {path: '/about-us', name: 'AboutUs', component: AboutUs},
    {path: '/faq', name: 'FAQ', component: Faq},
    {path: '/terms-conditions', name: 'TermsAndConditions', component: TermsAndConditions},
    {path: '/privacy-policy', name: 'PrivacyPolicy', component: PrivacyPolicy},
    {path: '/fraud-policy', name: 'FraudPolicy', component: FraudPolicy},
    {path: '/contact', name: 'ContactUs', component: ContactUs},
    {path: '/request-withdrawal/:id/:slug', name: 'RequestWithdrawal', component: RequestWithdrawal},
    {path: '/request-withdrawal-successful', name: 'WithdrawReqSuccess', component: WithdrawReqSuccess },
    {path: '*', name: 'Home', component: 'Home'}
]