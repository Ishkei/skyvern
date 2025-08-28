#!/usr/bin/env python3
"""
Create a comprehensive TopSurveys automation workflow for Skyvern.
This workflow handles the complete survey process including login, qualification,
and completion with persona-based responses.
"""

import asyncio
import json
import requests

def create_topsurveys_workflow():
    """Create the TopSurveys automation workflow using HTTP API"""

    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjQ5MDEzMjQ5MTksInN1YiI6Im9fNDMyNDI0Njk0MzQ4OTA4OTcwIn0.sBa1MnEliVTaGg5kd7qC7ovqLp7KWWYnALu2c-rSNkM"
    base_url = "http://localhost:8000"

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    # Define workflow parameters for persona customization
    parameters = [
        {
            "key": "survey_username",
            "description": "Username for TopSurveys login",
            "default_value": ""
        },
        {
            "key": "survey_password",
            "description": "Password for TopSurveys login",
            "default_value": ""
        },
        {
            "key": "persona_name",
            "description": "Name of the survey respondent",
            "default_value": "John Smith"
        },
        {
            "key": "persona_age",
            "description": "Age of the survey respondent",
            "default_value": "35"
        },
        {
            "key": "persona_gender",
            "description": "Gender of the survey respondent",
            "default_value": "Male"
        },
        {
            "key": "persona_income",
            "description": "Annual household income range",
            "default_value": "$50,000 - $74,999"
        },
        {
            "key": "persona_education",
            "description": "Education level",
            "default_value": "Bachelor's degree"
        },
        {
            "key": "persona_employment",
            "description": "Employment status",
            "default_value": "Full-time employed"
        },
        {
            "key": "persona_location",
            "description": "City and state of residence",
            "default_value": "New York, NY"
        },
        {
            "key": "max_surveys_per_run",
            "description": "Maximum number of surveys to complete per run",
            "default_value": "5"
        },
        {
            "key": "survey_delay_seconds",
            "description": "Delay between survey attempts (seconds)",
            "default_value": "10"
        }
    ]

    # Define the workflow blocks
    workflow_blocks = [
        # Block 1: Navigate to TopSurveys main page
        {
            "block_type": "navigation",
            "name": "navigate_to_topsurveys",
            "label": "Navigate to TopSurveys",
            "description": "Navigate to the TopSurveys main page",
            "data": {
                "navigation_goal": "Navigate to https://app.topsurveys.app/Surveys and wait for the page to load completely.",
                "url": "https://app.topsurveys.app/Surveys",
                "complete_criterion": "The TopSurveys dashboard or login page is visible",
                "terminate_criterion": "Page fails to load or shows an error message"
            }
        },

        # Block 2: Login to TopSurveys
        {
            "block_type": "login",
            "name": "login_to_topsurveys",
            "label": "Login to TopSurveys",
            "description": "Login using provided credentials",
            "data": {
                "navigation_goal": "Login to TopSurveys using the provided username and password. Look for login form and submit credentials.",
                "username": "{{survey_username}}",
                "password": "{{survey_password}}",
                "complete_criterion": "Successfully logged in and can see the surveys dashboard",
                "terminate_criterion": "Login fails or invalid credentials error is shown"
            }
        },

        # Block 3: Scan available surveys
        {
            "block_type": "task",
            "name": "scan_available_surveys",
            "label": "Scan Available Surveys",
            "description": "Scan and list all available surveys on the page",
            "data": {
                "navigation_goal": "Scan all available surveys on the page. Look for survey listings, titles, and any qualification requirements. Extract information about each survey including estimated time, payout, and basic requirements.",
                "data_extraction_schema": {
                    "surveys": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "url": {"type": "string"},
                                "estimated_time": {"type": "string"},
                                "payout": {"type": "string"},
                                "qualification_requirements": {"type": "string"}
                            }
                        }
                    }
                },
                "complete_criterion": "All surveys have been scanned and information extracted",
                "terminate_criterion": "No surveys available or page structure prevents scanning"
            }
        },

        # Block 4: ForLoop - Process each survey
        {
            "block_type": "for_loop",
            "name": "process_surveys_loop",
            "label": "Process Surveys Loop",
            "description": "Loop through available surveys and attempt to complete them",
            "data": {
                "loop_over": "{{scan_available_surveys_output.surveys}}",
                "loop_variable": "current_survey",
                "max_iterations": "{{max_surveys_per_run}}"
            },
            "blocks": [
                # Block 4.1: Navigate to survey
                {
                    "block_type": "navigation",
                    "name": "navigate_to_survey",
                    "label": "Navigate to Survey",
                    "description": "Navigate to the selected survey URL",
                    "data": {
                        "navigation_goal": "Navigate to the survey URL: {{current_survey.url}}",
                        "url": "{{current_survey.url}}",
                        "complete_criterion": "Survey page loads and pre-screening questions are visible",
                        "terminate_criterion": "Survey URL is invalid or page fails to load"
                    }
                },

                # Block 4.2: Check qualification status
                {
                    "block_type": "validation",
                    "name": "check_qualification_status",
                    "label": "Check Qualification Status",
                    "description": "Check if user qualifies for this survey",
                    "data": {
                        "validation_goal": "Check if the survey shows qualification status. Look for messages like 'you qualified', 'you did not qualify', or pre-screening questions.",
                        "validation_schema": {
                            "qualification_status": {
                                "type": "string",
                                "enum": ["qualified", "disqualified", "prescreening_required", "unknown"]
                            },
                            "message": {"type": "string"}
                        },
                        "complete_criterion": "Qualification status is determined",
                        "terminate_criterion": "Cannot determine qualification status"
                    }
                },

                # Block 4.3: Conditional - Handle qualified surveys
                {
                    "block_type": "task",
                    "name": "handle_qualified_survey",
                    "label": "Handle Qualified Survey",
                    "description": "Process survey if user qualified",
                    "condition": "{{check_qualification_status_output.qualification_status == 'qualified' or check_qualification_status_output.qualification_status == 'prescreening_required'}}",
                    "data": {
                        "navigation_goal": "Complete the survey by answering all questions based on the provided persona information. Answer questions naturally and truthfully based on the persona profile. If you encounter open-ended questions, provide thoughtful responses that align with the persona characteristics.",
                        "data_extraction_schema": {
                            "survey_progress": {
                                "type": "object",
                                "properties": {
                                    "current_question": {"type": "string"},
                                    "total_questions": {"type": "string"},
                                    "completion_percentage": {"type": "string"}
                                }
                            }
                        },
                        "complete_criterion": "Survey is completed or user is redirected to completion page",
                        "terminate_criterion": "Survey cannot be completed due to technical issues or disqualification during survey"
                    }
                },

                # Block 4.4: Conditional - Handle disqualified surveys
                {
                    "block_type": "task",
                    "name": "handle_disqualified_survey",
                    "label": "Handle Disqualified Survey",
                    "description": "Handle survey disqualification",
                    "condition": "{{check_qualification_status_output.qualification_status == 'disqualified'}}",
                    "data": {
                        "navigation_goal": "Acknowledge disqualification message and return to survey list. Look for 'did not qualify' or similar messages and navigate back to the main surveys page.",
                        "complete_criterion": "Returned to surveys list or main dashboard",
                        "terminate_criterion": "Cannot navigate back to surveys list"
                    }
                },

                # Block 4.5: Wait between surveys
                {
                    "block_type": "wait",
                    "name": "wait_between_surveys",
                    "label": "Wait Between Surveys",
                    "description": "Wait before processing next survey",
                    "data": {
                        "wait_seconds": "{{survey_delay_seconds}}"
                    }
                }
            ]
        },

        # Block 5: Check if we should continue
        {
            "block_type": "validation",
            "name": "check_completion_criteria",
            "label": "Check Completion Criteria",
            "description": "Check if we should continue processing more surveys",
            "data": {
                "validation_goal": "Check if there are more surveys available and if we haven't reached the maximum limit. Look for navigation options to load more surveys or return to the main survey page.",
                "validation_schema": {
                    "more_surveys_available": {"type": "boolean"},
                    "current_completion_count": {"type": "integer"},
                    "should_continue": {"type": "boolean"}
                },
                "complete_criterion": "Completion criteria are evaluated",
                "terminate_criterion": "Cannot determine completion status"
                    }
                },

        # Block 6: Final summary
        {
            "block_type": "task",
            "name": "generate_completion_summary",
            "label": "Generate Completion Summary",
            "description": "Generate a summary of completed surveys and results",
            "data": {
                "navigation_goal": "Create a summary of all survey attempts including successes, failures, and disqualifications. Navigate to the account dashboard if available to capture final statistics.",
                "data_extraction_schema": {
                    "summary": {
                        "type": "object",
                        "properties": {
                            "total_surveys_attempted": {"type": "integer"},
                            "surveys_completed": {"type": "integer"},
                            "surveys_disqualified": {"type": "integer"},
                            "total_earnings": {"type": "string"},
                            "completion_rate": {"type": "string"}
                        }
                    }
                },
                "complete_criterion": "Summary is generated and workflow is ready to complete",
                "terminate_criterion": "Cannot generate summary"
            }
        }
    ]

    # Create the workflow data in the format expected by Skyvern API
    workflow_data = {
        "title": "TopSurveys Automation Workflow",
        "description": "Automated workflow for completing surveys on TopSurveys platform with persona-based responses",
        "parameters": parameters,
        "blocks": workflow_blocks
    }

    try:
        # Create the workflow using HTTP API
        response = requests.post(
            f"{base_url}/api/v1/workflows",
            headers=headers,
            json=workflow_data
        )

        if response.status_code == 200:
            workflow_info = response.json()
            print("✅ TopSurveys workflow created successfully!")
            print(f"Workflow ID: {workflow_info.get('workflow_id')}")
            print(f"Workflow URL: http://localhost:8080/workflows/{workflow_info.get('workflow_id')}")

            # Save workflow information
            with open("/home/soto/skyvern/topsurveys_workflow_info.json", "w") as f:
                json.dump({
                    "workflow_id": workflow_info.get('workflow_id'),
                    "title": workflow_data["title"],
                    "description": workflow_data["description"],
                    "created_at": workflow_info.get('created_at')
                }, f, indent=2)

            return workflow_info
        else:
            print(f"❌ Failed to create workflow: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return None

    except Exception as e:
        print(f"❌ Failed to create workflow: {e}")
        raise

def main():
    """Main function to run the workflow creation"""
    try:
        workflow = create_topsurveys_workflow()
        if workflow:
            print("\n🎉 Workflow created successfully!")
            print("You can now run this workflow from the Skyvern UI or API.")
        else:
            print("\n❌ Workflow creation failed.")

    except Exception as e:
        print(f"❌ Error creating workflow: {e}")

if __name__ == "__main__":
    main()
