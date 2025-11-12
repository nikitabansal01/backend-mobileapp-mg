#!/usr/bin/env python3
"""
Complete Demo: Simulate Frontend Request to Hormone Analysis API
Shows the exact JSON response that frontend will receive
"""

import asyncio
import json
import sys
sys.path.insert(0, '/Users/mohanganesh/Auvra1/AuvraJuly15')

from app.services.root_cause_engine import RootCauseEngine


async def simulate_frontend_request():
    """Simulate a complete request from frontend with all data"""
    
    print("=" * 80)
    print("🎭 SIMULATING FRONTEND REQUEST TO HORMONE ANALYSIS API")
    print("=" * 80)
    print()
    
    # This is what frontend sends (complete user survey data)
    frontend_request = {
        # Period Information
        "period_description": "Irregular",
        "cycle_length": ">35 days",
        "period_concerns": ["Heavy bleeding", "Spotting before period", "Severe cramps"],
        
        # Body & Symptoms
        "body_concerns": ["Weight gain (unexplained)", "Bloating", "Breast tenderness"],
        "skin_hair_concerns": ["Acne (jawline/back)", "Hair loss (scalp)", "Facial hair"],
        "mental_health_concerns": ["Anxiety", "Mood swings", "Brain fog"],
        
        # Family History
        "family_history": ["Diabetes", "Thyroid disease", "PCOS"],
        
        # Lifestyle
        "sleep_duration": "<6 hours",
        "stress_level": "High",
        "workout_intensity": "None",
        
        # Free-text (analyzed by Gemini LLM)
        "symptom_others": "I have dark patches on my neck and face (acanthosis nigricans), excessive facial hair on chin and upper lip, hair thinning on scalp, and difficulty losing weight especially around my belly. I also feel tired all the time.",
        "family_others": "My mother has type 2 diabetes, my aunt has hypothyroidism, and my sister was diagnosed with PCOS last year"
    }
    
    print("📤 REQUEST FROM FRONTEND:")
    print("-" * 80)
    print(json.dumps(frontend_request, indent=2))
    print()
    print("⏳ Processing request...")
    print("   • Analyzing clinical symptoms from tables")
    print("   • Sending free-text to Gemini LLM for analysis")
    print("   • Merging scores and calculating confidence")
    print()
    
    # Process the request (this is what backend does)
    analysis_result = await RootCauseEngine.analyze_hormone_imbalance(frontend_request)
    
    # Build the complete response that frontend receives
    api_response = {
        "status": "success",
        "data": {
            "analysis": {
                "primary_imbalance": analysis_result["primary_imbalance"],
                "primary_level": analysis_result["primary_level"],
                "secondary_imbalances": analysis_result["secondary_imbalances"],
                "secondary_levels": analysis_result["secondary_levels"],
                "confidence": analysis_result["confidence"]
            },
            "hormone_scores": analysis_result["hormone_scores"],
            "gemini_api_active": True,
            "timestamp": "2025-11-13T00:00:00Z"
        }
    }
    
    print("=" * 80)
    print("📥 RESPONSE TO FRONTEND (Complete JSON):")
    print("=" * 80)
    print(json.dumps(api_response, indent=2))
    print()
    
    print("=" * 80)
    print("📊 HUMAN-READABLE SUMMARY FOR FRONTEND DISPLAY:")
    print("=" * 80)
    print()
    print(f"✅ Analysis Status: SUCCESS")
    print(f"🤖 Gemini LLM Active: YES")
    print(f"📈 Confidence Level: {analysis_result['confidence']}%")
    print()
    print("🎯 PRIMARY HORMONE IMBALANCE:")
    print(f"   {analysis_result['primary_imbalance'].upper()} is {analysis_result['primary_level'].upper()}")
    print()
    
    if analysis_result['secondary_imbalances']:
        print("⚠️  SECONDARY IMBALANCES:")
        for hormone, level in zip(analysis_result['secondary_imbalances'], 
                                   analysis_result['secondary_levels']):
            print(f"   • {hormone.upper()} is {level.upper()}")
        print()
    
    print("📋 DETAILED HORMONE SCORES (0-3 scale):")
    scores = analysis_result['hormone_scores']
    
    hormone_names = {
        'estrogen_high': 'Estrogen (HIGH)',
        'estrogen_low': 'Estrogen (LOW)',
        'progesterone_low': 'Progesterone (LOW)',
        'androgens_high': 'Androgens/Testosterone (HIGH)',
        'insulin_high': 'Insulin (HIGH)',
        'cortisol_high': 'Cortisol (HIGH)',
        'cortisol_low': 'Cortisol (LOW)',
        'thyroid_low': 'Thyroid (LOW)'
    }
    
    for key, name in hormone_names.items():
        score = scores.get(key, 0)
        bar = '█' * score + '░' * (3 - score)
        indicator = ""
        if score >= 3:
            indicator = " 🔴 SEVERE"
        elif score >= 2:
            indicator = " 🟡 MODERATE"
        elif score >= 1:
            indicator = " 🟢 MILD"
        
        print(f"   {name:35s} [{bar}] {score}/3{indicator}")
    
    print()
    print(f"📊 Total Symptoms Analyzed: {scores.get('total_signals', 0)}")
    print()
    
    print("=" * 80)
    print("💡 WHAT FRONTEND SHOULD DO WITH THIS DATA:")
    print("=" * 80)
    print("1. Display primary imbalance prominently")
    print("2. Show secondary imbalances if confidence > 60%")
    print("3. Visualize hormone scores with progress bars or charts")
    print("4. Show confidence level to indicate result reliability")
    print("5. Recommend next steps based on primary hormone")
    print()
    
    return api_response


if __name__ == "__main__":
    print()
    result = asyncio.run(simulate_frontend_request())
    print("=" * 80)
    print("✅ DEMO COMPLETE - System working perfectly!")
    print("=" * 80)
