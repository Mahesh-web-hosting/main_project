from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
	       path('CompanyLogin.html', views.CompanyLogin, name="CompanyLogin"), 
	       path('CompanyLoginAction.html', views.CompanyLoginAction, name="CompanyLoginAction"),
	       path('UserLogin', views.UserLogin, name="UserLogin"),
	       path('UserLoginAction', views.UserLoginAction, name="UserLoginAction"),	   
	       path('Signup', views.Signup, name="Signup"),
	       path('SignupAction', views.SignupAction, name="SignupAction"),
	       path('ResumeSelection', views.ResumeSelection, name="ResumeSelection"),
	       path('ResumeSelectionAction', views.ResumeSelectionAction, name="ResumeSelectionAction"),
	       path('AnalyseResume', views.AnalyseResume, name="AnalyseResume"),
	       path('AnalyseResumeAction', views.AnalyseResumeAction, name="AnalyseResumeAction"),
	       path('CreateResume', views.CreateResume, name="CreateResume"),
	       path('Aboutus', views.Aboutus, name="Aboutus"),
	       path('OTPValidation', views.OTPValidation, name="OTPValidation"),
]