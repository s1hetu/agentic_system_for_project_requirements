import os, uuid
import shutil
from pathlib import Path
from functools import wraps
from langchain_openai import ChatOpenAI
from msal import ConfidentialClientApplication
from django.http import FileResponse, JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect, render

from .individual_agents.main import EntityList
from .templatetags.markdown_extras import markdown_format
from .constants import ASK_QUESTIONS_TEMPLATE, REQUIREMENTS_TEMPLATE, GENERATE_SCOPE_TEMPLATE, KEY_OBJECTIVES_TEMPLATE, \
    TECH_STACK_TEMPLATE, DELIVERABLES_TEMPLATE, PROJECT_UNDERSTANDING_TEMPLATE, TIMELINE_TEMPLATE, \
    NFR_TEMPLATE, QUALITY_ASSURANCE_TEMPLATE, RISK_MANAGEMENT_TEMPLATE, COMPLIANCE_TEMPLATE, TESTING_PLAN_TEMPLATE, \
    TRAINING_PLAN_TEMPLATE, SUPPORT_AND_MAINTENANCE_TEMPLATE, EXECUTION_METHODOLOGY_TEMPLATE, TEST_TEMPLATE, \
    HOME_TEMPLATE, ERROR_TEMPLATE, PANELS_TEMPLATE, MODULES_TEMPLATE, MODULE_GENERATION_TEMPLATE, \
    ACTIONS_GENERATION_TEMPLATE, ACTIONS_TEMPLATE, TECH_STACK_INSTRUCTIONS, ACTIONS_INSTRUCTIONS, MODULES_INSTRUCTIONS, \
    PANELS_INSTRUCTIONS, DELIVERABLES_INSTRUCTIONS, KEY_OBJECTIVES_INSTRUCTIONS, PROJECT_UNDERSTANDING_INSTRUCTIONS, \
    QUESTIONS_INSTRUCTIONS, SUPPORT_AND_MAINTENANCE_INSTRUCTIONS, TRAINING_INSTRUCTIONS, TESTING_INSTRUCTIONS, \
    EXECUTION_METHODOLOGY_INSTRUCTIONS, COMPLIANCE_INSTRUCTIONS, RISK_MANAGEMENT_INSTRUCTIONS, \
    QUALITY_ASSURANCE_INSTRUCTIONS, NFR_INSTRUCTIONS, TIMELINE_INSTRUCTIONS
from .base_models import QuestionsModel, TimeLineModel, NonFunctionalRequirements
from .forms import GenerateContentForm, RequirementForm, PanelForm, ModuleForm
from .utils import get_logger, generate_document, handle_form
from django.utils.safestring import mark_safe
logger = get_logger("views")
openai_fastest_llm = ChatOpenAI(model="gpt-4.1-nano", api_key=os.environ.get('OPENAI_API_KEY'))


def ms_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.session.get('is_authenticated'):
            return redirect('ms_login')
        return view_func(request, *args, **kwargs)

    return _wrapped


def ms_login(request):
    # Create MSAL app
    try:
        msal_app = ConfidentialClientApplication(
            client_id=settings.MSAL_CLIENT_ID,
            client_credential=settings.MSAL_CLIENT_SECRET,
            authority=settings.MSAL_AUTHORITY,
        )
        # Build auth URL
        state = str(uuid.uuid4())
        request.session['auth_state'] = state
        auth_url = msal_app.get_authorization_request_url(
            scopes=settings.MSAL_SCOPE,
            state=state,
            redirect_uri=settings.MSAL_REDIRECT_URI
        )
        return redirect(auth_url)
    except Exception as error:
        logger.error(f"Error occurred while login - {error}")
        return render(request, ERROR_TEMPLATE, {'error': error})


def ms_callback(request):
    try:
        # Validate state
        if request.GET.get('state') != request.session.get('auth_state'):
            return redirect('ms_login')
        msal_app = ConfidentialClientApplication(
            client_id=settings.MSAL_CLIENT_ID,
            client_credential=settings.MSAL_CLIENT_SECRET,
            authority=settings.MSAL_AUTHORITY,
        )
        # Exchange code for token
        result = msal_app.acquire_token_by_authorization_code(
            code=request.GET.get('code'),
            scopes=settings.MSAL_SCOPE,
            redirect_uri=settings.MSAL_REDIRECT_URI
        )
        if 'id_token' in result:
            # Mark session as authenticated
            request.session['is_authenticated'] = True
            request.session['user_name'] = result.get('id_token_claims', {}).get('name')
            return redirect('generate-scope')
        return render(request, ERROR_TEMPLATE, {'error': result.get('error_description')})
    except Exception as error:
        logger.error(f"Error occurred while login - {error}")
        return render(request, ERROR_TEMPLATE, {'error': error})


class HomeView(View):
    def get(self, request):
        logger.info("Request: Home, Method: GET")
        return render(request, HOME_TEMPLATE, {})


class TestView(View):
    def get(self, request):
        logger.info("Request: Test, Method: GET")
        return render(request, TEST_TEMPLATE, {"mo": "TEST"})


@method_decorator(ms_required, name='dispatch')
class GenerateScopeView(View):
    def get(self, request):
        logger.info("Request: Generate Scope, Method: GET")
        return render(request, GENERATE_SCOPE_TEMPLATE, {'form': RequirementForm()})

    def post(self, request):
        logger.info("Request: Generate Scope, Method: POST")
        user_id = f"user_{str(uuid.uuid4()).replace('-', '_')}"
        try:
            form = RequirementForm(request.POST, request.FILES)
            if not form.is_valid():
                message = f"Invalid form submission: {form.errors.get('requirement_doc')[0]}"
                messages.error(request, message)
                logger.error(message)
                return redirect("generate-scope")
            form_text = form.cleaned_data['requirement_text']
            form_file = form.cleaned_data['requirement_doc']
            questions_doc = form.cleaned_data['questions_doc']
            response = generate_document(form_file, form_text, questions_doc, user_id)
            message = response.get("message")
            output = response.get("output")
            if output:
                message = "Returning Document successfully."
                logger.info(message)
                message += f"<br><a href='/download/scope/{user_id}/'>Click here to download</a>"
                messages.success(request, mark_safe(message))
                return redirect("generate-scope")
            else:
                logger.error(message)
                return render(request, GENERATE_SCOPE_TEMPLATE,
                              context={'form': RequirementForm(), "messages": message})
        except Exception as error:
            message = f"Exception occurred : {error}"
            messages.error(request, message)
            logger.error(message)
            return redirect("generate-scope")


class DownloadScopeView(View):
    def get(self, request, user_id):
        logger.info("Request: Download Scope, Method: GET")
        try:
            scope_file = f"{Path(__file__).resolve().parent.parent}/scope_pipeline/{user_id}/all_content.md"
            binary_scope_file = open(scope_file, 'rb')
            shutil.rmtree(f"{Path(__file__).resolve().parent.parent}/scope_pipeline/{user_id}")
            return FileResponse(
                binary_scope_file,
                as_attachment=True,
                filename="scope.md",
                content_type='text/markdown'
            )
        except FileNotFoundError:
            return HttpResponse("File not found", status=404)



@method_decorator(ms_required, name='dispatch')
class GenerateQuestions(View):

    def get(self, request):
        logger.info("Request: Generate Questions, Method: GET")
        return render(request, REQUIREMENTS_TEMPLATE, {'form': RequirementForm()})

    def post(self, request):
        logger.info("Request: Generate Questions, Method: POST")
        try:
            form = RequirementForm(request.POST, request.FILES)
            if not form.is_valid():
                message = f"Invalid form submission: {form.errors.get('requirement_doc')[0]}"
                messages.error(request, message)
                logger.error(message)
                return redirect("prepare-questions")

            user_input = request.POST.get('user_input')
            response_data = handle_form(form, QUESTIONS_INSTRUCTIONS,
                                        output_format=QuestionsModel,
                                        user_input=user_input,
                                        original_text=request.POST.get('original_text'))
            response = response_data.get('output')
            message = response_data.get('message')
            context = {
                "explanation": None,
                "questions": [],
                "messages": message
            }
            if response:
                logger.info(message)
                data = response.get('structured_response')
                context['explanation'] = data.explanation
                question_list = None
                questions = data.questions
                for question in questions:
                    if question_list is None:
                        question_list = []
                    question_list.append(question.question)
                context['questions'] = question_list
                context['messages'] = message
                if user_input:
                    return JsonResponse(context)
                else:
                    return render(request, ASK_QUESTIONS_TEMPLATE, context)
            else:
                logger.error(message)
                if user_input:
                    return JsonResponse(context)
                else:
                    messages.error(request, message)
                    return redirect("prepare-questions")
        except Exception as error:
            message = f"Exception occurred : {error}"
            messages.error(request, message)
            logger.error(message)
            return redirect("prepare-questions")


@method_decorator(ms_required, name='dispatch')
class GenerateProjectUnderstanding(View):
    def get(self, request):
        logger.info("Request: Generate Understanding, Method: GET")
        return render(request, REQUIREMENTS_TEMPLATE, {'form': RequirementForm()})

    def post(self, request):
        logger.info("Request: Generate Understanding, Method: POST")
        try:
            form = RequirementForm(request.POST, request.FILES)
            if not form.is_valid():
                message = f"Invalid form submission: {form.errors.get('requirement_doc')[0]}"
                messages.error(request, message)
                logger.error(message)
                return redirect("prepare-understanding")

            user_input = request.POST.get('user_input')
            response_data = handle_form(form, PROJECT_UNDERSTANDING_INSTRUCTIONS,
                                        user_input=request.POST.get('user_input'),
                                        original_text=request.POST.get('original_text'))
            response = response_data.get('output')
            message = response_data.get('message')
            if response:
                logger.info(message)
                data = response.get('messages')[-1].content
                if user_input:
                    return JsonResponse({"data": markdown_format(data), "messages": message})
                else:
                    return render(request,
                                  PROJECT_UNDERSTANDING_TEMPLATE,
                                  context={"data": data, "messages": message})
            else:
                logger.error(message)
                if user_input:
                    return JsonResponse(
                        {"data": "Unable to receive response for project understanding.", "messages": message})
                else:
                    messages.error(request, message)
                    return redirect("prepare-understanding")

        except Exception as error:
            message = f"Exception occurred : {error}"
            messages.error(request, message)
            logger.error(message)
            return redirect("prepare-understanding")


@method_decorator(ms_required, name='dispatch')
class GenerateKeyObjectives(View):

    def get(self, request):
        logger.info("Request: Generate Objectives, Method: GET")
        return render(request, REQUIREMENTS_TEMPLATE, {'form': RequirementForm()})

    def post(self, request):
        logger.info("Request: Generate Objectives, Method: POST")
        try:
            form = RequirementForm(request.POST, request.FILES)
            if not form.is_valid():
                message = f"Invalid form submission: {form.errors.get('requirement_doc')[0]}"
                messages.error(request, message)
                logger.error(message)
                return redirect("prepare-objectives")

            user_input = request.POST.get('user_input')
            response_data = handle_form(form, KEY_OBJECTIVES_INSTRUCTIONS,
                                        user_input=request.POST.get('user_input'),
                                        original_text=request.POST.get('original_text'))
            response = response_data.get('output')
            message = response_data.get('message')
            if response:
                logger.info(message)
                data = response.get('messages')[-1].content
                if user_input:
                    return JsonResponse({"data": markdown_format(data), "messages": message})
                else:
                    return render(request,
                                  KEY_OBJECTIVES_TEMPLATE,
                                  context={"data": data, "messages": message})
            else:
                logger.error(message)
                if user_input:
                    return JsonResponse({"data": "Unable to receive response for key objectives", "messages": message})
                else:
                    messages.error(request, message)
                    return redirect("prepare-objectives")
        except Exception as error:
            message = f"Exception occurred : {error}"
            messages.error(request, message)
            logger.error(message)
            return redirect("prepare-objectives")


@method_decorator(ms_required, name='dispatch')
class GenerateDeliverables(View):
    def get(self, request):
        logger.info("Request: Generate Deliverables, Method: GET")
        return render(request, REQUIREMENTS_TEMPLATE, {'form': RequirementForm()})

    def post(self, request):
        logger.info("Request: Generate Deliverables, Method: POST")
        try:
            form = RequirementForm(request.POST, request.FILES)
            if not form.is_valid():
                message = f"Invalid form submission: {form.errors.get('requirement_doc')[0]}"
                messages.error(request, message)
                logger.error(message)
                return redirect("prepare-deliverables")

            user_input = request.POST.get('user_input')
            response_data = handle_form(form, DELIVERABLES_INSTRUCTIONS,
                                        user_input=user_input,
                                        original_text=request.POST.get('original_text'))

            response = response_data.get('output')
            message = response_data.get('message')
            if response:
                logger.info(message)
                data = response.get('messages')[-1].content
                if user_input:
                    return JsonResponse({"data": markdown_format(data), "messages": message})
                else:
                    return render(request,
                                  DELIVERABLES_TEMPLATE,
                                  context={"data": data, "messages": message})
            else:
                logger.error(message)
                if user_input:
                    return JsonResponse({"data": "Unable to receive response for deliverables", "messages": message})
                else:
                    messages.error(request, message)
                    return redirect("prepare-deliverables")
        except Exception as error:
            message = f"Exception occurred : {error}"
            messages.error(request, message)
            logger.error(message)
            return redirect("prepare-deliverables")


@method_decorator(ms_required, name='dispatch')
class GeneratePanels(View):
    def get(self, request):
        logger.info("Request: Generate Panels, Method: GET")
        return render(request, REQUIREMENTS_TEMPLATE, {'form': RequirementForm()})

    def post(self, request):
        logger.info("Request: Generate Panels, Method: POST")
        try:
            form = RequirementForm(request.POST, request.FILES)
            if not form.is_valid():
                message = f"Invalid form submission: {form.errors.get('requirement_doc')[0]}"
                messages.error(request, message)
                logger.error(message)
                return redirect("prepare-panels")

            user_input = request.POST.get('user_input')
            response_data = handle_form(form, PANELS_INSTRUCTIONS,
                                        user_input=user_input,
                                        original_text=request.POST.get('original_text'))

            response = response_data.get('output')
            message = response_data.get('message')
            if response:
                logger.info(message)
                data = response['messages'][-1].content
                if user_input:
                    return JsonResponse({"data": markdown_format(data), "messages": message})
                else:
                    return render(request,
                                  PANELS_TEMPLATE,
                                  context={"data": markdown_format(data), "messages": message})
            else:
                logger.error(message)
                if user_input:
                    return JsonResponse({"data": "Unable to receive response for panels", "messages": message})
                else:
                    messages.error(request, message)
                    return redirect("prepare-panels")
        except Exception as error:
            message = f"Exception occurred : {error}"
            messages.error(request, message)
            logger.error(message)
            return redirect("prepare-panels")


@method_decorator(ms_required, name='dispatch')
class GenerateModules(View):
    def get(self, request):
        logger.info("Request: Generate Modules, Method: GET")
        return render(request, MODULE_GENERATION_TEMPLATE, {'form': PanelForm()})

    def post(self, request):
        logger.info("Request: Generate Modules, Method: POST")
        try:
            form = PanelForm(request.POST, request.FILES)
            if not form.is_valid():
                message = f"Invalid form submission: {form.errors.get('requirement_doc')[0]}"
                messages.error(request, message)
                logger.error(message)
                return redirect("prepare-modules")

            user_input = request.POST.get('user_input')
            panel_details = request.POST.get('panel')
            response_data = handle_form(form, MODULES_INSTRUCTIONS,
                                        user_input=user_input, output_format=EntityList,
                                        original_text=request.POST.get('original_text'),
                                        panel_details=panel_details)

            response = response_data.get('output')
            message = response_data.get('message')
            if response:
                logger.info(message)
                data = response['messages'][-1].content
                if user_input:
                    return JsonResponse({"data": markdown_format(data), "messages": message})
                else:
                    return render(request,
                                  MODULES_TEMPLATE,
                                  context={"data": markdown_format(data), "messages": message})
            else:
                logger.error(message)
                if user_input:
                    return JsonResponse({"data": "Unable to receive response for modules", "messages": message})
                else:
                    messages.error(request, message)
                    return redirect("prepare-modules")
        except Exception as error:
            message = f"Exception occurred : {error}"
            messages.error(request, message)
            logger.error(message)
            return redirect("prepare-modules")


@method_decorator(ms_required, name='dispatch')
class GenerateActions(View):
    def get(self, request):
        logger.info("Request: Generate Actions, Method: GET")
        return render(request, ACTIONS_GENERATION_TEMPLATE, {'form': ModuleForm()})

    def post(self, request):
        logger.info("Request: Generate Actions, Method: POST")
        try:
            form = ModuleForm(request.POST, request.FILES)
            if not form.is_valid():
                message = f"Invalid form submission: {form.errors.get('requirement_doc')[0]}"
                messages.error(request, message)
                logger.error(message)
                return redirect("prepare-actions")

            user_input = request.POST.get('user_input')
            panel_details = request.POST.get('panel')
            module_details = request.POST.get('module')

            response_data = handle_form(form, ACTIONS_INSTRUCTIONS,
                                        user_input=user_input,
                                        original_text=request.POST.get('original_text'),
                                        panel_details=panel_details,
                                        module_details=module_details
                                        )

            response = response_data.get('output')
            message = response_data.get('message')
            if response:
                logger.info(message)
                data = response.get('messages')[-1].content
                if user_input:
                    return JsonResponse({"data": markdown_format(data), "messages": message})
                else:
                    return render(request,
                                  ACTIONS_TEMPLATE,
                                  context={"data": data, "messages": message})
            else:
                logger.error(message)
                if user_input:
                    return JsonResponse({"data": "Unable to receive response for actions", "messages": message})
                else:
                    messages.error(request, message)
                    return redirect("prepare-actions")
        except Exception as error:
            message = f"Exception occurred : {error}"
            messages.error(request, message)
            logger.error(message)
            return redirect("prepare-actions")


@method_decorator(ms_required, name='dispatch')
class GenerateTechStack(View):
    def get(self, request):
        logger.info("Request: Generate TechStack, Method: GET")
        return render(request, REQUIREMENTS_TEMPLATE, {'form': RequirementForm()})

    def post(self, request):
        logger.info("Request: Generate TechStack, Method: POST")
        try:
            form = RequirementForm(request.POST, request.FILES)
            if not form.is_valid():
                message = f"Invalid form submission: {form.errors.get('requirement_doc')[0]}"
                messages.error(request, message)
                logger.error(message)
                return redirect("prepare-tech-stack")

            user_input = request.POST.get('user_input')
            response_data = handle_form(form, TECH_STACK_INSTRUCTIONS,
                                        user_input=request.POST.get('user_input'),
                                        original_text=request.POST.get('original_text'))
            response = response_data.get('output')
            message = response_data.get('message')
            if response:
                logger.info(message)
                data = response.get('messages')[-1].content
                if user_input:
                    return JsonResponse({"data": markdown_format(data), "messages": message})
                else:
                    return render(request,
                                  TECH_STACK_TEMPLATE,
                                  context={"data": markdown_format(data), "messages": message})
            else:
                logger.error(message)
                if user_input:
                    return JsonResponse({"data": "Unable to receive response for tech stack", "messages": message})
                else:
                    messages.error(request, message)
                    return redirect("prepare-tech-stack")
        except Exception as error:
            message = f"Exception occurred : {error}"
            messages.error(request, message)
            logger.error(message)
            return redirect("prepare-tech-stack")


@method_decorator(ms_required, name='dispatch')
class GenerateTimeline(View):
    def get(self, request):
        logger.info("Request: Generate Timeline, Method: GET")
        return render(request, REQUIREMENTS_TEMPLATE, {'form': RequirementForm()})

    def post(self, request):
        logger.info("Request: Generate Timeline, Method: POST")
        try:
            form = RequirementForm(request.POST, request.FILES)
            if not form.is_valid():
                message = f"Invalid form submission: {form.errors.get('requirement_doc')[0]}"
                messages.error(request, message)
                logger.error(message)
                return redirect("prepare-timeline")

            user_input = request.POST.get('user_input')
            response_data = handle_form(form, TIMELINE_INSTRUCTIONS,
                                        output_format=TimeLineModel,
                                        user_input=request.POST.get('user_input'),
                                        original_text=request.POST.get('original_text'))
            response = response_data.get('output')
            message = response_data.get('message')
            data_response = {
                "table": None,
                "duration": None,
                "summary": None,
                "resources": None,
                "messages": message
            }

            if response:
                logger.info(message)
                data = response.get('structured_response')
                table = []
                data_table = data.table
                for entry in data_table:
                    phase = entry.phase
                    data_features = [i.feature for i in entry.features]
                    duration = entry.duration
                    resources = [i.developer for i in entry.resources]
                    table.append([phase, data_features, duration, resources])
                resources = {}
                data_resources = data.resources
                for resource in data_resources:
                    dev = resource.developer.developer
                    count = resource.count
                    resources[dev] = count
                duration = data.project_duration
                summary = data.summary
                data_response.update({
                    "table": table,
                    "duration": duration,
                    "summary": summary,
                    "resources": resources,
                    "messages": message
                })
                if user_input:
                    return JsonResponse(data_response)
                else:
                    return render(request,
                                  TIMELINE_TEMPLATE,
                                  context=data_response)
            else:
                logger.error(message)
                if user_input:
                    return JsonResponse(data_response)
                else:
                    messages.error(request, message)
                    return redirect("prepare-timeline")

        except Exception as error:
            message = f"Exception occurred : {error}"
            messages.error(request, message)
            logger.error(message)
            return redirect("prepare-timeline")


@method_decorator(ms_required, name='dispatch')
class GenerateQualityAssurance(View):
    def get(self, request):
        logger.info("Request: Generate Quality Assurance, Method: GET")
        return render(request, REQUIREMENTS_TEMPLATE, {'form': RequirementForm()})

    def post(self, request):
        logger.info("Request: Generate Quality Assurance, Method: POST")
        try:
            form = RequirementForm(request.POST, request.FILES)
            if not form.is_valid():
                message = f"Invalid form submission: {form.errors.get('requirement_doc')[0]}"
                messages.error(request, message)
                logger.error(message)
                return redirect("prepare-quality-assurance")

            user_input = request.POST.get('user_input')
            response_data = handle_form(form, QUALITY_ASSURANCE_INSTRUCTIONS,
                                        user_input=user_input,
                                        original_text=request.POST.get('original_text')
                                        )
            response = response_data.get('output')
            message = response_data.get('message')
            if response:
                logger.info(message)
                data = response.get('messages')[-1].content
                if user_input:
                    return JsonResponse({"data": markdown_format(data), "messages": message})
                else:
                    return render(request, QUALITY_ASSURANCE_TEMPLATE, {"data": data, "messages": message})
            else:
                logger.error(message)
                if user_input:
                    return JsonResponse(
                        {"data": "Unable to receive response for quality assurance.", "messages": message})
                else:
                    messages.error(request, message)
                    return redirect("prepare-quality-assurance")
        except Exception as error:
            message = f"Exception occurred : {error}"
            messages.error(request, message)
            logger.error(message)
            return redirect("prepare-quality-assurance")


@method_decorator(ms_required, name='dispatch')
class GenerateRiskManagement(View):
    def get(self, request):
        logger.info("Request: Generate Risk Management, Method: GET")
        return render(request, REQUIREMENTS_TEMPLATE, {'form': RequirementForm()})

    def post(self, request):
        logger.info("Request: Generate Risk Management, Method: POST")
        try:
            form = RequirementForm(request.POST, request.FILES)
            if not form.is_valid():
                message = f"Invalid form submission: {form.errors.get('requirement_doc')[0]}"
                messages.error(request, message)
                logger.error(message)
                return redirect('prepare-risk-management')

            user_input = request.POST.get('user_input')
            response_data = handle_form(form, RISK_MANAGEMENT_INSTRUCTIONS,
                                        user_input=user_input,
                                        original_text=request.POST.get('original_text')
                                        )
            response = response_data.get('output')
            message = response_data.get('message')
            if response:
                logger.info(message)
                data = response.get('messages')[-1].content
                if user_input:
                    return JsonResponse({"data": markdown_format(data), "messages": message})
                else:
                    return render(request,
                                  RISK_MANAGEMENT_TEMPLATE,
                                  context={"data": markdown_format(data), "messages": message})
            else:
                logger.error(message)
                if user_input:
                    return JsonResponse(
                        {"data": "Unable to receive response for risk management.", "messages": message})
                else:
                    messages.error(request, message)
                    return redirect('prepare-risk-management')
        except Exception as error:
            message = f"Exception occurred : {error}"
            messages.error(request, message)
            logger.error(message)
            return redirect('prepare-risk-management')


@method_decorator(ms_required, name='dispatch')
class GenerateCompliance(View):
    def get(self, request):
        logger.info("Request: Generate Compliance, Method: GET")
        return render(request, REQUIREMENTS_TEMPLATE, {'form': RequirementForm()})

    def post(self, request):
        logger.info("Request: Generate Compliance, Method: POST")
        try:
            form = RequirementForm(request.POST, request.FILES)
            if not form.is_valid():
                message = f"Invalid form submission: {form.errors.get('requirement_doc')[0]}"
                messages.error(request, message)
                logger.error(message)
                return redirect("prepare-compliance")

            user_input = request.POST.get('user_input')
            response_data = handle_form(form, COMPLIANCE_INSTRUCTIONS,
                                        user_input=user_input,
                                        original_text=request.POST.get('original_text')
                                        )
            response = response_data.get('output')
            message = response_data.get('message')
            if response:
                logger.info(message)
                data = response.get('messages')[-1].content
                if user_input:
                    return JsonResponse({"data": markdown_format(data), "messages": message})
                else:
                    return render(request,
                                  COMPLIANCE_TEMPLATE,
                                  context={"data": data, "messages": message})
            else:
                logger.error(message)
                if user_input:
                    return JsonResponse({"data": "Unable to receive response for compliance.", "messages": message})
                else:
                    messages.error(request, message)
                    return redirect("prepare-compliance")
        except Exception as error:
            message = f"Exception occurred : {error}"
            messages.error(request, message)
            logger.error(message)
            return redirect("prepare-compliance")


@method_decorator(ms_required, name='dispatch')
class GenerateExecutionMethodology(View):
    def get(self, request):
        logger.info("Request: Generate Execution Methodology, Method: GET")
        return render(request, REQUIREMENTS_TEMPLATE, {'form': RequirementForm()})

    def post(self, request):
        logger.info("Request: Generate Execution Methodology, Method: POST")
        try:
            form = RequirementForm(request.POST, request.FILES)
            if not form.is_valid():
                message = f"Invalid form submission: {form.errors.get('requirement_doc')[0]}"
                messages.error(request, message)
                logger.error(message)
                return redirect("prepare-execution-methodology")

            user_input = request.POST.get('user_input')
            response_data = handle_form(form, EXECUTION_METHODOLOGY_INSTRUCTIONS,
                                        user_input=user_input,
                                        original_text=request.POST.get('original_text')
                                        )
            response = response_data.get('output')
            message = response_data.get('message')
            if response:
                logger.info(message)
                data = response.get('messages')[-1].content
                if user_input:
                    return JsonResponse({"data": markdown_format(data), "messages": message})
                else:
                    return render(request,
                                  EXECUTION_METHODOLOGY_TEMPLATE,
                                  context={"data": data, "messages": message})
            else:
                logger.error(message)
                if user_input:
                    return JsonResponse(
                        {"data": "Unable to receive response for execution methodology.", "messages": message})
                else:
                    messages.error(request, message)
                    return redirect("prepare-execution-methodology")
        except Exception as error:
            message = f"Exception occurred : {error}"
            messages.error(request, message)
            logger.error(message)
            return redirect("prepare-execution-methodology")


@method_decorator(ms_required, name='dispatch')
class GenerateTestingPlan(View):
    def get(self, request):
        logger.info("Request: Generate Testing Plan, Method: GET")
        return render(request, REQUIREMENTS_TEMPLATE, {'form': RequirementForm()})

    def post(self, request):
        logger.info("Request: Generate Testing Plan, Method: POST")
        try:
            form = RequirementForm(request.POST, request.FILES)
            if not form.is_valid():
                message = f"Invalid form submission: {form.errors.get('requirement_doc')[0]}"
                messages.error(request, message)
                logger.error(message)
                return redirect("prepare-testing-plan")

            user_input = request.POST.get('user_input')
            response_data = handle_form(form, TESTING_INSTRUCTIONS,
                                        user_input=user_input,
                                        original_text=request.POST.get('original_text')
                                        )
            response = response_data.get('output')
            message = response_data.get('message')

            if response:
                logger.info(message)
                data = response.get('messages')[-1].content
                if user_input:
                    return JsonResponse({"data": markdown_format(data), "messages": message})
                else:
                    return render(request,
                                  TESTING_PLAN_TEMPLATE,
                                  context={"data": data, "messages": message})
            else:
                logger.error(message)
                if user_input:
                    return JsonResponse({"data": "Unable to receive response for testing plan.", "messages": message})
                else:
                    messages.error(request, message)
                    return redirect("prepare-testing-plan")
        except Exception as error:
            message = f"Exception occurred : {error}"
            messages.error(request, message)
            logger.error(message)
            return redirect("prepare-testing-plan")


@method_decorator(ms_required, name='dispatch')
class GenerateTrainingPlan(View):
    def get(self, request):
        logger.info("Request: Generate Training Plan, Method: GET")
        return render(request, REQUIREMENTS_TEMPLATE, {'form': RequirementForm()})

    def post(self, request):
        logger.info("Request: Generate Training Plan, Method: POST")
        try:
            form = RequirementForm(request.POST, request.FILES)
            if not form.is_valid():
                message = f"Invalid form submission: {form.errors.get('requirement_doc')[0]}"
                messages.error(request, message)
                logger.error(message)
                return redirect("prepare-training-plan")

            user_input = request.POST.get('user_input')
            response_data = handle_form(form, TRAINING_INSTRUCTIONS,
                                        user_input=user_input,
                                        original_text=request.POST.get('original_text')
                                        )
            response = response_data.get('output')
            message = response_data.get('message')
            if response:
                logger.info(message)
                data = response.get('messages')[-1].content
                if user_input:
                    return JsonResponse({"data": markdown_format(data), "messages": message})
                else:
                    return render(request,
                                  TRAINING_PLAN_TEMPLATE,
                                  context={"data": data, "messages": message})
            else:
                logger.error(message)
                if user_input:
                    return JsonResponse({"data": "Unable to receive response for training plan.", "messages": message})
                else:
                    messages.error(request, message)
                    return redirect("prepare-training-plan")
        except Exception as error:
            message = f"Exception occurred : {error}"
            messages.error(request, message)
            logger.error(message)
            return redirect("prepare-training-plan")


@method_decorator(ms_required, name='dispatch')
class GenerateSupportAndMaintenance(View):
    def get(self, request):
        logger.info("Request: Generate Support & Maintenance, Method: GET")
        return render(request, REQUIREMENTS_TEMPLATE, {'form': RequirementForm()})

    def post(self, request):
        logger.info("Request: Generate Support & Maintenance, Method: POST")
        try:
            form = RequirementForm(request.POST, request.FILES)
            if not form.is_valid():
                message = f"Invalid form submission: {form.errors.get('requirement_doc')[0]}"
                messages.error(request, message)
                logger.error(message)
                return redirect("prepare-support-maintenance")

            user_input = request.POST.get('user_input')
            response_data = handle_form(form, SUPPORT_AND_MAINTENANCE_INSTRUCTIONS,
                                        user_input=user_input,
                                        original_text=request.POST.get('original_text')
                                        )
            response = response_data.get('output')
            message = response_data.get('message')
            if response:
                logger.info(message)
                data = response.get('messages')[-1].content
                if user_input:
                    return JsonResponse({"data": markdown_format(data), "messages": message})
                else:
                    return render(request,
                                  SUPPORT_AND_MAINTENANCE_TEMPLATE,
                                  context={"data": data, "messages": message})
            else:
                logger.error(message)
                if user_input:
                    return JsonResponse(
                        {"data": "Unable to receive response for support and maintenance.", "messages": message})
                else:
                    messages.error(request, message)
                    return redirect("prepare-support-maintenance")
        except Exception as error:
            message = f"Exception occurred : {error}"
            messages.error(request, message)
            logger.error(message)
            return redirect("prepare-support-maintenance")


@method_decorator(ms_required, name='dispatch')
class GenerateNonFunctionalRequirements(View):
    def get(self, request):
        logger.info("Request: Generate NFR, Method: GET")
        return render(request, REQUIREMENTS_TEMPLATE, {'form': RequirementForm()})

    def post(self, request):
        logger.info("Request: Generate NFR, Method: POST")
        try:
            form = RequirementForm(request.POST, request.FILES)
            if not form.is_valid():
                message = f"Invalid form submission: {form.errors.get('requirement_doc')[0]}"
                messages.error(request, message)
                logger.error(message)
                return redirect("prepare-nfr")

            user_input = request.POST.get('user_input')
            response_data = handle_form(form, NFR_INSTRUCTIONS, output_format=NonFunctionalRequirements,
                                        user_input=user_input,
                                        original_text=request.POST.get('original_text')
                                        )
            response = response_data.get('output')
            message = response_data.get('message')
            data = {"quality_assurance": None,
                    "risk_management": None,
                    "compliance": None,
                    "execution_methodology": None,
                    "testing": None,
                    "training_plan": None,
                    "support_and_maintenance": None,
                    "messages": message
                    }
            if response:
                logger.info(message)
                raw_data = response.get('structured_response')
                data.update({"quality_assurance": raw_data.quality_assurance,
                             "risk_management": raw_data.risk_management,
                             "compliance": raw_data.compliance,
                             "execution_methodology": raw_data.execution_methodology,
                             "testing": raw_data.testing,
                             "training_plan": raw_data.training_plan,
                             "support_and_maintenance": raw_data.support_and_maintenance,
                             "messages": message
                             })
                if user_input:
                    return JsonResponse(data)
                else:
                    return render(request, NFR_TEMPLATE, data)
            else:
                logger.error(message)
                if user_input:
                    return JsonResponse(data)
                else:
                    messages.error(request, message)
                    return redirect("prepare-nfr")
        except Exception as error:
            message = f"Exception occurred : {error}"
            messages.error(request, message)
            logger.error(message)
            return redirect("prepare-nfr")
