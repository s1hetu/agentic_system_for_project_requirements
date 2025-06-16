from django.urls import path
from .views import GenerateScopeView, HomeView, ms_login, ms_callback, GenerateQuestions, GenerateTechStack, \
    GenerateKeyObjectives, GenerateProjectUnderstanding, GenerateDeliverables, TestView, GenerateTimeline, \
    GenerateNonFunctionalRequirements, GenerateQualityAssurance, GenerateRiskManagement, GenerateCompliance, \
    GenerateExecutionMethodology, GenerateTestingPlan, GenerateTrainingPlan, GenerateSupportAndMaintenance, \
    GeneratePanels, GenerateModules, GenerateActions, DownloadScopeView

urlpatterns = [

    # healthcheck
    path('', HomeView.as_view(), name="home"),
    # test
    path('test', TestView.as_view(), name="test"),
    # microsoft auth
    path('ms_login', ms_login, name="ms_login"),
    path('msal/callback/', ms_callback, name='ms_callback'),
    # scope
    path('scope/', GenerateScopeView.as_view(), name="generate-scope"),
    # download scope document
    path("download/scope/<str:user_id>/", DownloadScopeView.as_view(), name="download-scope"),
    # questions
    path('prepare_questions/', GenerateQuestions.as_view(), name="prepare-questions"),
    # project understanding
    path('prepare_understanding/', GenerateProjectUnderstanding.as_view(), name="prepare-understanding"),
    # key objectives
    path('prepare_objectives/', GenerateKeyObjectives.as_view(), name="prepare-objectives"),
    # deliverables
    path('prepare_deliverables/', GenerateDeliverables.as_view(), name="prepare-deliverables"),
    # panels/interfaces
    path('prepare_panels/', GeneratePanels.as_view(), name="prepare-panels"),
    # panel modules
    path('prepare_modules/', GenerateModules.as_view(), name="prepare-modules"),
    # panel module actions
    path('prepare_actions/', GenerateActions.as_view(), name="prepare-actions"),
    # tech stack
    path('prepare_tech_stack/', GenerateTechStack.as_view(), name="prepare-tech-stack"),
    # timeline
    path('prepare_timeline/', GenerateTimeline.as_view(), name="prepare-timeline"),
    # non-functional requirements
    path('prepare_nfr/', GenerateNonFunctionalRequirements.as_view(), name="prepare-nfr"),
    # quality assurance
    path('prepare_quality_assurance/', GenerateQualityAssurance.as_view(), name="prepare-quality-assurance"),
    # risk management
    path('prepare_risk_management/', GenerateRiskManagement.as_view(), name="prepare-risk-management"),
    # compliance
    path('prepare_compliance/', GenerateCompliance.as_view(), name="prepare-compliance"),
    # execution methodology
    path('prepare_execution_methodology/', GenerateExecutionMethodology.as_view(), name="prepare-execution-methodology"),
    # testing plan
    path('prepare_testing_plan/', GenerateTestingPlan.as_view(), name="prepare-testing-plan"),
    # training plan
    path('prepare_training_plan/', GenerateTrainingPlan.as_view(), name="prepare-training-plan"),
    # support and maintenance
    path('prepare_support_maintenance/', GenerateSupportAndMaintenance.as_view(), name="prepare-support-maintenance"),

]
