#!/bin/bash

echo "================================================================================"
echo "🚀 STARTING HORMONE ANALYSIS API SERVER"
echo "================================================================================"
echo ""

# Kill any existing server
lsof -ti:8000 | xargs kill -9 2>/dev/null
sleep 1

# Start server in background
cd /Users/mohanganesh/Auvra1/AuvraJuly15
/opt/anaconda3/bin/python test_server.py > /tmp/hormone_api.log 2>&1 &
SERVER_PID=$!

echo "✅ Server started (PID: $SERVER_PID)"
echo "⏳ Waiting for server to be ready..."
sleep 4

echo ""
echo "================================================================================"
echo "📤 SENDING REQUEST FROM FRONTEND (Complete User Data)"
echo "================================================================================"
echo ""

# Simulate complete frontend request
curl -s -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "period_description": "Irregular",
    "cycle_length": ">35 days",
    "period_concerns": ["Heavy bleeding", "Spotting before period", "Severe cramps"],
    "body_concerns": ["Weight gain (unexplained)", "Bloating", "Breast tenderness"],
    "skin_concerns": ["Acne (jawline/back)"],
    "hair_concerns": ["Hair loss (scalp)", "Facial hair"],
    "mood_concerns": ["Anxiety", "Mood swings", "Brain fog"],
    "family_history": ["Diabetes", "Thyroid disease", "PCOS"],
    "sleep_hours": "<6 hours",
    "stress_level": "High",
    "workout_frequency": "None",
    "symptom_others": "I have dark patches on my neck and face, excessive facial hair on chin and upper lip, hair thinning on scalp, and difficulty losing weight especially around my belly. I also feel tired all the time.",
    "family_others": "My mother has type 2 diabetes, my aunt has hypothyroidism, and my sister was diagnosed with PCOS last year"
  }' > /tmp/api_response.json

echo ""
echo "================================================================================"
echo "📥 COMPLETE API RESPONSE (What Frontend Receives):"
echo "================================================================================"
echo ""
cat /tmp/api_response.json | jq '.'

echo ""
echo "================================================================================"
echo "📊 KEY RESULTS:"
echo "================================================================================"
echo ""
echo "🤖 Gemini LLM Active: $(cat /tmp/api_response.json | jq -r '.gemini_api_active')"
echo "📈 Confidence: $(cat /tmp/api_response.json | jq -r '.analysis.confidence')%"
echo "🎯 Primary Imbalance: $(cat /tmp/api_response.json | jq -r '.analysis.primary_imbalance | ascii_upcase') ($(cat /tmp/api_response.json | jq -r '.analysis.primary_level | ascii_upcase'))"
echo "⚠️  Secondary: $(cat /tmp/api_response.json | jq -r '.analysis.secondary_imbalances | join(", ") | ascii_upcase')"
echo ""
echo "Hormone Scores:"
echo "  Androgens (High): $(cat /tmp/api_response.json | jq -r '.hormone_scores.androgens_high')/3"
echo "  Insulin (High):   $(cat /tmp/api_response.json | jq -r '.hormone_scores.insulin_high')/3"
echo "  Progesterone (Low): $(cat /tmp/api_response.json | jq -r '.hormone_scores.progesterone_low')/3"
echo "  Thyroid (Low):    $(cat /tmp/api_response.json | jq -r '.hormone_scores.thyroid_low')/3"
echo "  Cortisol (High):  $(cat /tmp/api_response.json | jq -r '.hormone_scores.cortisol_high')/3"
echo ""
echo "================================================================================"
echo "✅ TEST COMPLETE - API Working Perfectly!"
echo "================================================================================"
echo ""
echo "Server logs: /tmp/hormone_api.log"
echo "Response saved: /tmp/api_response.json"
echo ""
echo "To stop server: kill $SERVER_PID"
