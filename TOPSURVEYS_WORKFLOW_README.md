# TopSurveys Automation Workflow

This Skyvern workflow automates the complete process of completing surveys on TopSurveys platform with persona-based responses and intelligent qualification handling.

## 🚀 Features

- **Complete Survey Automation**: Handles login, survey scanning, qualification checking, and completion
- **Persona-Based Responses**: Customizable demographic and personal information for consistent survey responses
- **Intelligent Qualification Logic**: Automatically detects and handles qualified/disqualified surveys
- **Survey Router Navigation**: Handles complex survey routing and redirects
- **Loop-Based Processing**: Continues processing surveys with configurable limits and delays
- **Comprehensive Error Handling**: Robust error handling for various survey scenarios
- **Progress Tracking**: Extracts and tracks survey completion statistics

## 📋 Prerequisites

1. **Skyvern Installation**: Ensure Skyvern is properly installed and running
2. **TopSurveys Account**: Valid TopSurveys account with login credentials
3. **Persona Information**: Demographic data for survey responses

## 🛠️ Setup Instructions

### Step 1: Start Skyvern Server

```bash
cd /home/soto/skyvern
poetry run skyvern run api
```

Wait for the server to start on `http://localhost:8000`

### Step 2: Create the Workflow

Run the creation script:

```bash
chmod +x create_workflow_curl.sh
./create_workflow_curl.sh
```

Or create manually via Skyvern UI:
1. Go to `http://localhost:8080`
2. Navigate to Workflows section
3. Import the `topsurveys_workflow.yaml` file

### Step 3: Configure Parameters

When running the workflow, you'll need to provide:

**Login Credentials:**
- `survey_username`: Your TopSurveys username
- `survey_password`: Your TopSurveys password

**Persona Information:**
- `persona_name`: Respondent's full name (default: "John Smith")
- `persona_age`: Age (default: "35")
- `persona_gender`: Gender (default: "Male")
- `persona_income`: Income range (default: "$50,000 - $74,999")
- `persona_education`: Education level (default: "Bachelor's degree")
- `persona_employment`: Employment status (default: "Full-time employed")
- `persona_location`: City and state (default: "New York, NY")

**Workflow Settings:**
- `max_surveys_per_run`: Maximum surveys to complete (default: "5")
- `survey_delay_seconds`: Delay between surveys (default: "10")

## 🎯 Workflow Process

### 1. **Navigation to TopSurveys**
- Navigates to https://app.topsurveys.app/Surveys
- Waits for page to load completely

### 2. **Login Process**
- Locates and fills login form
- Submits credentials
- Verifies successful login

### 3. **Survey Scanning**
- Scans all available surveys on the dashboard
- Extracts survey information:
  - Survey titles
  - URLs
  - Estimated completion time
  - Payout amounts
  - Qualification requirements

### 4. **Survey Processing Loop**
For each available survey:

#### **Qualification Check**
- Navigates to survey URL
- Checks qualification status:
  - **Qualified**: Proceeds to survey completion
  - **Disqualified**: Acknowledges and returns to survey list
  - **Pre-screening Required**: Processes pre-screening questions

#### **Survey Completion**
- Answers all questions based on persona information
- Handles various question types:
  - Multiple choice
  - Rating scales
  - Open-ended questions (provides thoughtful responses)
  - Demographic questions
- Navigates survey routers and handles redirects
- Continues until survey completion or disqualification

#### **Delay Management**
- Waits specified seconds between surveys
- Prevents rate limiting

### 5. **Completion Summary**
- Generates summary of all survey attempts
- Tracks successes, failures, and disqualifications
- Calculates completion statistics and earnings

## 📝 Response Guidelines

The workflow follows these response guidelines to maintain authenticity:

### **Character Restrictions**
- No special characters: `-`, `/`, `[`, `]`, `(`, `)`, `!`, `@`, `#`, `$`, `%`, `^`, `&`, `*`, `+`, `=`, `\`, `|`
- Clean text only: Letters, numbers, spaces, basic punctuation
- Natural language responses without automation terms

### **Content Filtering**
- No bot references: Avoids "automation", "bot", "script" terms
- No technical jargon: Keeps responses accessible
- Context-appropriate: Matches response style to question type
- Emotionally intelligent: Appropriate emotional responses

### **Response Templates**
```python
# Example filtered response
"Based on my experience, I find that people often prefer
simple solutions that work reliably. When I think about
this topic, I consider how it affects daily life and
what would make the most sense for most people."
```

## 🔧 Customization

### **Modifying Persona Information**
Edit the workflow parameters to customize:
- Demographic information
- Personal preferences
- Response patterns
- Behavioral characteristics

### **Adjusting Workflow Behavior**
- Change `max_surveys_per_run` for different batch sizes
- Modify `survey_delay_seconds` for different pacing
- Add additional validation blocks for specific scenarios

### **Adding Survey Platforms**
The workflow can be extended to support additional survey platforms by:
1. Adding new navigation blocks for different sites
2. Creating platform-specific login handlers
3. Implementing platform-specific qualification logic

## 📊 Output Data

The workflow extracts and provides:

### **Survey Information**
```json
{
  "surveys": [
    {
      "title": "Consumer Electronics Survey",
      "url": "https://app.topsurveys.app/survey/123",
      "estimated_time": "10 minutes",
      "payout": "$2.50",
      "qualification_requirements": "Must own smartphone"
    }
  ]
}
```

### **Qualification Status**
```json
{
  "qualification_status": "qualified|disqualified|prescreening_required|unknown",
  "message": "Detailed qualification message"
}
```

### **Completion Summary**
```json
{
  "summary": {
    "total_surveys_attempted": 5,
    "surveys_completed": 3,
    "surveys_disqualified": 2,
    "total_earnings": "$7.50",
    "completion_rate": "60%"
  }
}
```

## 🚨 Error Handling

The workflow includes comprehensive error handling for:

- **Login failures**: Invalid credentials or login form issues
- **Network timeouts**: Page loading or connection issues
- **Qualification failures**: Survey disqualification scenarios
- **Technical issues**: Browser errors or page structure changes
- **Rate limiting**: Automatic delays and retry logic

## 🔄 Loop Logic

The workflow implements intelligent looping:

- **Survey Iteration**: Processes each available survey
- **Router Navigation**: Handles multi-step survey routers
- **Redirect Handling**: Manages survey completion redirects
- **Continuation Logic**: Determines when to stop processing

## 🎛️ Running the Workflow

### **Via Skyvern UI**
1. Navigate to the workflow in Skyvern UI
2. Click "Run Workflow"
3. Fill in all required parameters
4. Monitor execution in real-time

### **Via API**
```bash
curl -X POST "http://localhost:8000/api/v1/workflows/{workflow_id}/run" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "parameters": {
      "survey_username": "your_username",
      "survey_password": "your_password",
      "persona_name": "John Doe",
      "persona_age": "28",
      "persona_gender": "Male",
      "max_surveys_per_run": "3"
    }
  }'
```

## 📈 Monitoring and Analytics

- **Real-time Progress**: Monitor survey completion progress
- **Success Metrics**: Track completion rates and earnings
- **Error Logging**: Detailed error information for troubleshooting
- **Performance Analytics**: Execution time and efficiency metrics

## 🔒 Security Considerations

- **Credential Management**: Securely handles login credentials
- **Session Management**: Properly manages browser sessions
- **Rate Limiting**: Implements delays to avoid detection
- **Data Privacy**: Persona information used only for survey completion

## 🐛 Troubleshooting

### **Common Issues**

1. **Login Failures**
   - Verify TopSurveys credentials
   - Check if account has unusual login requirements
   - Ensure account is not suspended

2. **Survey Loading Issues**
   - Check internet connection
   - Verify TopSurveys site availability
   - Look for browser compatibility issues

3. **Qualification Problems**
   - Review persona information accuracy
   - Check if survey requirements match persona
   - Consider updating demographic parameters

4. **Rate Limiting**
   - Increase `survey_delay_seconds`
   - Reduce `max_surveys_per_run`
   - Run workflow during off-peak hours

### **Debug Mode**
Enable detailed logging by modifying workflow blocks to include additional validation and extraction steps.

## 📚 Additional Resources

- **Skyvern Documentation**: https://docs.skyvern.com
- **Workflow Best Practices**: https://docs.skyvern.com/workflows/workflow-blocks-details
- **Parameter Usage**: https://docs.skyvern.com/workflows/workflow-parameters
- **Troubleshooting Guide**: https://docs.skyvern.com/getting-started/prompting-guide

## 🤝 Support

For issues with this workflow:
1. Check the troubleshooting section
2. Review Skyvern logs for error details
3. Verify all parameters are correctly configured
4. Test with a single survey before full automation

---

**⚠️ Important Note**: Always comply with TopSurveys terms of service and applicable laws when using automation tools. This workflow is designed for legitimate survey completion purposes only.
