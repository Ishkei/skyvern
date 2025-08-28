#!/bin/bash
# Create TopSurveys workflow using curl and the YAML definition

API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjQ5MDEzMjQ5MTksInN1YiI6Im9fNDMyNDI0Njk0MzQ4OTA4OTcwIn0.sBa1MnEliVTaGg5kd7qC7ovqLp7KWWYnALu2c-rSNkM"
BASE_URL="http://localhost:8000"

echo "Creating TopSurveys Automation Workflow..."

curl -X POST "${BASE_URL}/api/v1/workflows" \
  -H "x-api-key: ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d @topsurveys_workflow.yaml \
  -w "\nHTTP Status: %{http_code}\n" \
  -o workflow_response.json

if [ $? -eq 0 ]; then
    echo "✅ Workflow creation request sent successfully!"
    echo "Response saved to workflow_response.json"

    if [ -f workflow_response.json ]; then
        echo "Response:"
        cat workflow_response.json | python3 -m json.tool 2>/dev/null || cat workflow_response.json

        # Extract workflow ID if available
        WORKFLOW_ID=$(cat workflow_response.json | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('workflow_id', 'N/A'))" 2>/dev/null)
        if [ "$WORKFLOW_ID" != "N/A" ]; then
            echo ""
            echo "🎉 Workflow created successfully!"
            echo "Workflow ID: $WORKFLOW_ID"
            echo "Workflow URL: http://localhost:8080/workflows/$WORKFLOW_ID"
        fi
    fi
else
    echo "❌ Failed to create workflow"
fi
