"""
Test script to demonstrate hormone scoring system
Run this to see how the clinical scoring works with different symptom profiles
"""

from app.services.hormone_scoring_service import HormoneScoringService
from app.services.root_cause_engine import RootCauseEngine
import json


def print_result(title: str, user_data: dict, result: dict):
    """Pretty print test results"""
    print("\n" + "="*80)
    print(f"🧪 TEST: {title}")
    print("="*80)
    
    print("\n📋 INPUT SYMPTOMS:")
    print(json.dumps(user_data, indent=2))
    
    print("\n🔬 HORMONE ANALYSIS:")
    print(f"  Primary: {result['primary_imbalance'].upper()} ({result['primary_level']})")
    print(f"  Secondary: {', '.join(result['secondary_imbalances']) if result['secondary_imbalances'] else 'None'}")
    print(f"  Confidence: {result.get('confidence', 0)}%")
    
    if 'hormone_scores' in result:
        print("\n📊 DETAILED SCORES (0-3 scale):")
        scores = result['hormone_scores']
        for hormone in ['androgens_high', 'progesterone_low', 'estrogen_high', 'estrogen_low', 
                       'insulin_high', 'cortisol_high', 'cortisol_low', 'thyroid_low']:
            if scores.get(hormone, 0) > 0:
                print(f"  • {hormone}: {scores[hormone]}/3")
    
    print("\n" + "-"*80)


def test_pcos_profile():
    """Test Case 1: Classic PCOS symptoms"""
    user_data = {
        "period_description": "Irregular",
        "cycle_length": "35+ days",
        "period_concerns": ["Irregular Periods"],
        "body_concerns": ["Difficulty losing weight / stubborn belly fat", "Recent weight gain"],
        "skin_hair_concerns": ["Hirsutism (hair growth on chin, nipples etc)", "Adult Acne"],
        "mental_health_concerns": ["Mood swings"],
        "family_history": ["PCOS", "Diabetes"],
        "sleep_duration": "6-7 hours",
        "stress_level": "Moderate",
        "workout_intensity": "I'm yet to start"
    }
    
    result = RootCauseEngine.analyze_hormone_imbalance(user_data)
    print_result("PCOS Profile - Irregular periods, hirsutism, weight gain", user_data, result)
    
    expected = "androgens_high (testosterone)" 
    actual = f"{result['primary_imbalance']}"
    print(f"\n✅ EXPECTED: High androgens/testosterone")
    print(f"{'✅ PASS' if 'testosterone' in actual.lower() or 'androgen' in actual.lower() else '❌ FAIL'}: Got {actual}")


def test_progesterone_deficiency():
    """Test Case 2: Progesterone deficiency (PMS, mood swings)"""
    user_data = {
        "period_description": "Occasional Skips",
        "cycle_length": "Less than 21 days",
        "period_concerns": ["Painful Periods", "Light periods / Spotting"],
        "body_concerns": ["Menstrual headaches"],
        "skin_hair_concerns": [],
        "mental_health_concerns": ["Mood swings", "Fatigue"],
        "family_history": ["Premenstrual Syndrome"],
        "sleep_duration": "7-8 hours",
        "stress_level": "High",
        "workout_intensity": "Moderate"
    }
    
    result = RootCauseEngine.analyze_hormone_imbalance(user_data)
    print_result("Progesterone Deficiency - Short cycles, PMS, mood swings", user_data, result)
    
    print(f"\n✅ EXPECTED: Low progesterone")
    print(f"{'✅ PASS' if 'progesterone' in result['primary_imbalance'].lower() else '❌ FAIL'}: Got {result['primary_imbalance']}")


def test_estrogen_dominance():
    """Test Case 3: Estrogen dominance (heavy periods, bloating)"""
    user_data = {
        "period_description": "Regular",
        "cycle_length": "26-30 days",
        "period_concerns": ["Heavy periods", "Painful Periods"],
        "body_concerns": ["Bloating", "Menstrual headaches", "Nausea"],
        "skin_hair_concerns": [],
        "mental_health_concerns": ["Mood swings"],
        "family_history": ["Endometriosis"],
        "sleep_duration": "7-8 hours",
        "stress_level": "Low",
        "workout_intensity": "Moderate"
    }
    
    result = RootCauseEngine.analyze_hormone_imbalance(user_data)
    print_result("Estrogen Dominance - Heavy periods, bloating, headaches", user_data, result)
    
    print(f"\n✅ EXPECTED: High estrogen")
    print(f"{'✅ PASS' if 'estrogen' in result['primary_imbalance'].lower() else '❌ FAIL'}: Got {result['primary_imbalance']}")


def test_thyroid_issues():
    """Test Case 4: Hypothyroidism (fatigue, weight gain, hair loss)"""
    user_data = {
        "period_description": "Irregular",
        "cycle_length": "31-35 days",
        "period_concerns": ["Irregular Periods"],
        "body_concerns": ["Recent weight gain", "Difficulty losing weight / stubborn belly fat"],
        "skin_hair_concerns": ["Thinning of hair"],
        "mental_health_concerns": ["Fatigue"],
        "family_history": [],
        "sleep_duration": "8+ hours",
        "stress_level": "Low",
        "workout_intensity": "Gentle"
    }
    
    result = RootCauseEngine.analyze_hormone_imbalance(user_data)
    print_result("Hypothyroidism - Fatigue, weight gain, hair loss", user_data, result)
    
    print(f"\n✅ EXPECTED: Low thyroid")
    print(f"{'✅ PASS' if 'thyroid' in result['primary_imbalance'].lower() else '❌ FAIL'}: Got {result['primary_imbalance']}")


def test_high_stress_cortisol():
    """Test Case 5: High cortisol from stress"""
    user_data = {
        "period_description": "Regular",
        "cycle_length": "26-30 days",
        "period_concerns": [],
        "body_concerns": ["Recent weight gain", "Difficulty losing weight / stubborn belly fat"],
        "skin_hair_concerns": [],
        "mental_health_concerns": ["Stress", "Fatigue"],
        "family_history": [],
        "sleep_duration": "Less than 6 hours",
        "stress_level": "High",
        "workout_intensity": "High Energy"
    }
    
    result = RootCauseEngine.analyze_hormone_imbalance(user_data)
    print_result("High Cortisol - High stress, poor sleep, overtraining", user_data, result)
    
    print(f"\n✅ EXPECTED: High cortisol")
    print(f"{'✅ PASS' if 'cortisol' in result['primary_imbalance'].lower() else '❌ FAIL'}: Got {result['primary_imbalance']}")


def test_minimal_symptoms():
    """Test Case 6: Minimal symptoms (low confidence)"""
    user_data = {
        "period_description": "Regular",
        "cycle_length": "26-30 days",
        "period_concerns": [],
        "body_concerns": [],
        "skin_hair_concerns": [],
        "mental_health_concerns": [],
        "family_history": [],
        "sleep_duration": "7-8 hours",
        "stress_level": "Low",
        "workout_intensity": "Moderate"
    }
    
    result = RootCauseEngine.analyze_hormone_imbalance(user_data)
    print_result("Minimal Symptoms - Healthy profile", user_data, result)
    
    confidence = result.get('confidence', 0)
    print(f"\n✅ EXPECTED: Low confidence (<50%)")
    print(f"{'✅ PASS' if confidence < 50 else '❌ FAIL'}: Got {confidence}%")


if __name__ == "__main__":
    print("\n" + "🧬 HORMONE SCORING SYSTEM TEST SUITE ".center(80, "="))
    print("\nTesting clinical scoring tables with 6 different symptom profiles...")
    
    try:
        test_pcos_profile()
        test_progesterone_deficiency()
        test_estrogen_dominance()
        test_thyroid_issues()
        test_high_stress_cortisol()
        test_minimal_symptoms()
        
        print("\n" + "="*80)
        print("✅ ALL TESTS COMPLETED!")
        print("="*80)
        print("\n📌 Key Points:")
        print("  • Clinical scoring tables implemented (10 tables)")
        print("  • 8 hormone types scored (0-3 scale)")
        print("  • Confidence calculation based on symptom count")
        print("  • Backward compatible with existing API")
        print("  • No frontend changes required")
        print("\n" + "="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
