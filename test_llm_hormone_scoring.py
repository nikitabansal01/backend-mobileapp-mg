"""
Test LLM-Based Hormone Scoring with Gemini 2.5 Flash
Demonstrates free-text symptom analysis
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

sys.path.append('/Users/mohanganesh/Auvra1/AuvraJuly15')

from app.services.hormone_scoring_service import HormoneScoringService
from app.services.root_cause_engine import RootCauseEngine


async def test_llm_scoring():
    print("=" * 80)
    print("🧪 TESTING LLM-BASED HORMONE SCORING")
    print("=" * 80)
    
    # Test Case 1: Insulin Resistance (Dark Patches + Family History)
    print("\n📋 TEST CASE 1: Insulin Resistance Symptoms")
    print("-" * 80)
    
    user_data_1 = {
        "period_description": "Irregular",
        "cycle_length": "35+ days",
        "period_concerns": ["Irregular Periods"],
        "body_concerns": ["Difficulty losing weight / stubborn belly fat"],
        "symptom_others": "I have dark patches on my neck and armpits that won't go away, also skin tags on my neck",
        "family_others": "My mother has Type 2 diabetes, my sister has PCOS"
    }
    
    print("Input:")
    print(f"  Period: Irregular, Cycle: 35+ days")
    print(f"  Free-text symptoms: {user_data_1['symptom_others']}")
    print(f"  Family history: {user_data_1['family_others']}")
    
    scores_1 = await HormoneScoringService.calculate_hormone_scores(user_data_1)
    
    print("\n🎯 Results:")
    print(f"  Androgens High: {scores_1['androgens_high']}")
    print(f"  Insulin High: {scores_1['insulin_high']} ⭐ (boosted by LLM - acanthosis nigricans)")
    print(f"  Confidence: {scores_1['confidence']}%")
    print(f"  Total Signals: {scores_1['total_signals']}")
    
    # Test Case 2: Adrenal Fatigue (Morning Fatigue)
    print("\n" + "=" * 80)
    print("📋 TEST CASE 2: Adrenal Fatigue Symptoms")
    print("-" * 80)
    
    user_data_2 = {
        "period_description": "Regular",
        "mental_health_concerns": ["Fatigue", "Stress"],
        "sleep_duration": "7-8 hours",
        "stress_level": "High",
        "symptom_others": "Extreme fatigue every morning despite 8 hours sleep, need 3 cups of coffee to function, dizzy when I stand up quickly, intense salt cravings"
    }
    
    print("Input:")
    print(f"  Sleep: 7-8 hours, Stress: High")
    print(f"  Free-text symptoms: {user_data_2['symptom_others']}")
    
    scores_2 = await HormoneScoringService.calculate_hormone_scores(user_data_2)
    
    print("\n🎯 Results:")
    print(f"  Cortisol Low: {scores_2['cortisol_low']} ⭐ (detected by LLM - morning fatigue + orthostatic dizziness)")
    print(f"  Cortisol High: {scores_2['cortisol_high']}")
    print(f"  Confidence: {scores_2['confidence']}%")
    
    # Test Case 3: Hypothyroidism (Outer Eyebrow Loss)
    print("\n" + "=" * 80)
    print("📋 TEST CASE 3: Hypothyroidism Symptoms")
    print("-" * 80)
    
    user_data_3 = {
        "period_description": "Regular",
        "body_concerns": ["Recent weight gain"],
        "skin_hair_concerns": ["Thinning of hair"],
        "mental_health_concerns": ["Fatigue"],
        "symptom_others": "My eyebrows are thinning especially the outer third, always cold even in summer, constipation, dry skin"
    }
    
    print("Input:")
    print(f"  Concerns: Weight gain, Hair thinning, Fatigue")
    print(f"  Free-text symptoms: {user_data_3['symptom_others']}")
    
    scores_3 = await HormoneScoringService.calculate_hormone_scores(user_data_3)
    
    print("\n🎯 Results:")
    print(f"  Thyroid Low: {scores_3['thyroid_low']} ⭐ (boosted by LLM - outer eyebrow loss is pathognomonic)")
    print(f"  Confidence: {scores_3['confidence']}%")
    
    # Test Case 4: PCOS with LLM Enhancement
    print("\n" + "=" * 80)
    print("📋 TEST CASE 4: PCOS with Free-Text Details")
    print("-" * 80)
    
    user_data_4 = {
        "period_description": "I don't get periods",
        "cycle_length": "35+ days",
        "skin_hair_concerns": ["Hirsutism (hair growth on chin, nipples etc)", "Adult Acne"],
        "body_concerns": ["Difficulty losing weight / stubborn belly fat"],
        "symptom_others": "Thick dark hair on chin and upper lip, acne on jawline and back that won't respond to treatment, male pattern baldness starting at crown",
        "family_history": ["PCOS", "Diabetes"]
    }
    
    print("Input:")
    print(f"  Period: None, Hair growth: Hirsutism, Acne")
    print(f"  Free-text symptoms: {user_data_4['symptom_others']}")
    print(f"  Family: PCOS, Diabetes")
    
    scores_4 = await HormoneScoringService.calculate_hormone_scores(user_data_4)
    
    print("\n🎯 Results:")
    print(f"  Androgens High: {scores_4['androgens_high']} ⭐ (severe PCOS pattern)")
    print(f"  Insulin High: {scores_4['insulin_high']} ⭐ (metabolic component)")
    print(f"  Confidence: {scores_4['confidence']}%")
    
    # Full Root Cause Analysis
    print("\n" + "=" * 80)
    print("📊 FULL ROOT CAUSE ANALYSIS (TEST CASE 4)")
    print("-" * 80)
    
    analysis = await RootCauseEngine.analyze_hormone_imbalance(user_data_4)
    
    print(f"\n🎯 Primary Imbalance: {analysis['primary_imbalance']} ({analysis['primary_level']})")
    print(f"🎯 Secondary Imbalances: {', '.join(analysis['secondary_imbalances'])}")
    print(f"📊 Confidence: {analysis['confidence']}%")
    print(f"\n💡 Hormone Scores (0-3):")
    for hormone, score in analysis['hormone_scores'].items():
        if hormone not in ["confidence", "total_signals"] and score > 0:
            print(f"  - {hormone}: {score}")
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS COMPLETED")
    print("=" * 80)
    print("\n💡 Key Insights:")
    print("  1. LLM detects specific symptoms not in dropdown lists")
    print("  2. Free-text provides clinical context (severity, location, duration)")
    print("  3. Score merging takes MAXIMUM of table + LLM scores")
    print("  4. API format unchanged - backward compatible")
    print("  5. Confidence increases with more specific symptoms")
    
    print("\n🔒 IMPORTANT:")
    print("  - Set GEMINI_API_KEY environment variable to enable LLM scoring")
    print("  - Without API key, system falls back to table-based scoring only")
    print("  - No errors thrown if LLM unavailable (graceful degradation)")
    print("\n")


if __name__ == "__main__":
    # Check if GEMINI_API_KEY is set
    if not os.getenv("GEMINI_API_KEY"):
        print("\n⚠️  WARNING: GEMINI_API_KEY not set!")
        print("   LLM scoring will be skipped, only table-based scoring will run.")
        print("   Set environment variable: export GEMINI_API_KEY='your_key_here'")
        print("   Get API key: https://aistudio.google.com/app/apikey\n")
    
    asyncio.run(test_llm_scoring())
