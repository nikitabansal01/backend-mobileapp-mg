"""
Hormone Scoring Service
Implements clinical scoring tables for symptom-based hormone assessment
Based on: AUVRA HORMONE ASSESSMENT SYSTEM (v1 Clinical Review)
"""

from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class HormoneScoringService:
    """
    Clinical hormone scoring based on symptoms, lifestyle, and family history.
    Implements 10 scoring tables with 0-3 scale for 8 hormone types.
    """
    
    # ==================== SCORING TABLES ====================
    
    # TABLE 1: Period Description Scoring
    PERIOD_DESCRIPTION_SCORES = {
        "Regular": {},
        "Irregular": {
            "androgens_high": 2,
            "thyroid_low": 1
        },
        "Occasional Skips": {
            "androgens_high": 1,
            "progesterone_low": 1
        },
        "I don't get periods": {
            "androgens_high": 2,
            "estrogen_low": 2
        }
    }
    
    # TABLE 2: Cycle Length Scoring
    CYCLE_LENGTH_SCORES = {
        "Less than 21 days": {
            "progesterone_low": 2
        },
        "21-25 days": {},
        "26-30 days": {},
        "31-35 days": {
            "androgens_high": 1
        },
        "35+ days": {
            "androgens_high": 2,
            "insulin_high": 1
        }
    }
    
    # TABLE 3: Period Concerns Scoring
    PERIOD_CONCERNS_SCORES = {
        "Irregular Periods": {
            "androgens_high": 2,
            "thyroid_low": 1
        },
        "Painful Periods": {
            "estrogen_high": 2,
            "progesterone_low": 1
        },
        "Light periods / Spotting": {
            "estrogen_low": 2,
            "progesterone_low": 2
        },
        "Heavy periods": {
            "estrogen_high": 2,
            "progesterone_low": 1
        }
    }
    
    # TABLE 4: Body Concerns Scoring
    BODY_CONCERNS_SCORES = {
        "Bloating": {
            "estrogen_high": 1,
            "insulin_high": 1
        },
        "Hot Flashes": {
            "estrogen_low": 2
        },
        "Nausea": {
            "estrogen_high": 1,
            "cortisol_low": 1
        },
        "Difficulty losing weight / stubborn belly fat": {
            "insulin_high": 2,
            "cortisol_high": 1,
            "thyroid_low": 1
        },
        "Recent weight gain": {
            "insulin_high": 2,
            "thyroid_low": 2,
            "cortisol_high": 1
        },
        "Menstrual headaches": {
            "estrogen_high": 2,
            "progesterone_low": 1
        }
    }
    
    # TABLE 5: Skin & Hair Concerns Scoring
    SKIN_HAIR_CONCERNS_SCORES = {
        "Hirsutism (hair growth on chin, nipples etc)": {
            "androgens_high": 3  # Strongest marker
        },
        "Thinning of hair": {
            "thyroid_low": 2,
            "androgens_high": 1
        },
        "Adult Acne": {
            "androgens_high": 2,
            "insulin_high": 1
        }
    }
    
    # TABLE 6: Mental Health Concerns Scoring
    MENTAL_HEALTH_CONCERNS_SCORES = {
        "Mood swings": {
            "progesterone_low": 2,
            "estrogen_high": 1
        },
        "Stress": {
            "cortisol_high": 2
        },
        "Fatigue": {
            "thyroid_low": 2,
            "cortisol_low": 2,
            "insulin_high": 1
        }
    }
    
    # TABLE 7: Family History Boosters
    FAMILY_HISTORY_SCORES = {
        "Diabetes": {
            "insulin_high": 1
        },
        "PCOS": {
            "androgens_high": 1,
            "insulin_high": 1
        },
        "PCOD": {
            "androgens_high": 1,
            "insulin_high": 1
        },
        "Endometriosis": {
            "estrogen_high": 1
        },
        "Dysmenorrhea": {
            "estrogen_high": 1
        },
        "Amenorrhea": {
            "estrogen_low": 1
        },
        "Menorrhagia": {
            "estrogen_high": 1,
            "progesterone_low": 1
        },
        "Metrorrhagia": {
            "estrogen_high": 1
        },
        "Cushing's Syndrome": {
            "cortisol_high": 2
        },
        "Premenstrual Syndrome": {
            "progesterone_low": 1
        }
    }
    
    # TABLE 8: Sleep Hours Scoring
    SLEEP_DURATION_SCORES = {
        "Less than 6 hours": {
            "cortisol_high": 2,
            "insulin_high": 1
        },
        "<6 hours": {  # Alternative format
            "cortisol_high": 2,
            "insulin_high": 1
        },
        "6-7 hours": {
            "cortisol_high": 1
        },
        "7-8 hours": {},
        "8+ hours": {}
    }
    
    # TABLE 9: Stress Levels Scoring
    STRESS_LEVEL_SCORES = {
        "Low": {},
        "Moderate": {
            "cortisol_high": 1
        },
        "High": {
            "cortisol_high": 2,
            "progesterone_low": 1
        }
    }
    
    # TABLE 10: Workout Intensity Scoring
    WORKOUT_INTENSITY_SCORES = {
        "I'm yet to start": {
            "insulin_high": 1
        },
        "Gentle": {},
        "Moderate": {},
        "High Energy": {
            "cortisol_high": 1,
            "progesterone_low": 1
        },
        "I mix it up": {},
        # Alternative formats
        "Low": {},
        "High": {
            "cortisol_high": 1,
            "progesterone_low": 1
        }
    }
    
    # ==================== SCORING LOGIC ====================
    
    @staticmethod
    def calculate_hormone_scores(user_data: Dict) -> Dict:
        """
        Calculate 0-3 scores for 8 hormones based on clinical scoring tables.
        
        Args:
            user_data: Dictionary containing survey responses
            
        Returns:
            Dict with hormone scores (0-3) and confidence percentage
            {
                "estrogen_high": 2,
                "estrogen_low": 0,
                "progesterone_low": 3,
                "androgens_high": 2,
                "insulin_high": 1,
                "cortisol_high": 1,
                "cortisol_low": 0,
                "thyroid_low": 1,
                "confidence": 75,
                "total_signals": 12
            }
        """
        # Initialize all hormone scores to 0
        scores = {
            "estrogen_high": 0,
            "estrogen_low": 0,
            "progesterone_low": 0,
            "androgens_high": 0,
            "insulin_high": 0,
            "cortisol_high": 0,
            "cortisol_low": 0,
            "thyroid_low": 0
        }
        
        total_signals = 0  # Track how many symptoms were analyzed
        
        try:
            # TABLE 1: Period Description
            period_desc = user_data.get("period_description")
            if period_desc and period_desc in HormoneScoringService.PERIOD_DESCRIPTION_SCORES:
                HormoneScoringService._add_scores(
                    scores, 
                    HormoneScoringService.PERIOD_DESCRIPTION_SCORES[period_desc]
                )
                total_signals += 1
                logger.debug(f"Period description '{period_desc}' scored")
            
            # TABLE 2: Cycle Length
            cycle_length = user_data.get("cycle_length")
            if cycle_length and cycle_length in HormoneScoringService.CYCLE_LENGTH_SCORES:
                HormoneScoringService._add_scores(
                    scores, 
                    HormoneScoringService.CYCLE_LENGTH_SCORES[cycle_length]
                )
                total_signals += 1
                logger.debug(f"Cycle length '{cycle_length}' scored")
            
            # TABLE 3: Period Concerns (multi-select)
            period_concerns = user_data.get("period_concerns", [])
            if isinstance(period_concerns, list):
                for concern in period_concerns:
                    if concern in HormoneScoringService.PERIOD_CONCERNS_SCORES:
                        HormoneScoringService._add_scores(
                            scores, 
                            HormoneScoringService.PERIOD_CONCERNS_SCORES[concern]
                        )
                        total_signals += 1
                        logger.debug(f"Period concern '{concern}' scored")
            
            # TABLE 4: Body Concerns (multi-select)
            body_concerns = user_data.get("body_concerns", [])
            if isinstance(body_concerns, list):
                for concern in body_concerns:
                    if concern in HormoneScoringService.BODY_CONCERNS_SCORES:
                        HormoneScoringService._add_scores(
                            scores, 
                            HormoneScoringService.BODY_CONCERNS_SCORES[concern]
                        )
                        total_signals += 1
                        logger.debug(f"Body concern '{concern}' scored")
            
            # TABLE 5: Skin & Hair Concerns (multi-select)
            skin_hair_concerns = user_data.get("skin_hair_concerns", [])
            if isinstance(skin_hair_concerns, list):
                for concern in skin_hair_concerns:
                    if concern in HormoneScoringService.SKIN_HAIR_CONCERNS_SCORES:
                        HormoneScoringService._add_scores(
                            scores, 
                            HormoneScoringService.SKIN_HAIR_CONCERNS_SCORES[concern]
                        )
                        total_signals += 1
                        logger.debug(f"Skin/hair concern '{concern}' scored")
            
            # TABLE 6: Mental Health Concerns (multi-select)
            mental_concerns = user_data.get("mental_health_concerns", [])
            if isinstance(mental_concerns, list):
                for concern in mental_concerns:
                    if concern in HormoneScoringService.MENTAL_HEALTH_CONCERNS_SCORES:
                        HormoneScoringService._add_scores(
                            scores, 
                            HormoneScoringService.MENTAL_HEALTH_CONCERNS_SCORES[concern]
                        )
                        total_signals += 1
                        logger.debug(f"Mental health concern '{concern}' scored")
            
            # TABLE 7: Family History (multi-select)
            family_history = user_data.get("family_history", [])
            if isinstance(family_history, list):
                for condition in family_history:
                    if condition in HormoneScoringService.FAMILY_HISTORY_SCORES:
                        HormoneScoringService._add_scores(
                            scores, 
                            HormoneScoringService.FAMILY_HISTORY_SCORES[condition]
                        )
                        total_signals += 1
                        logger.debug(f"Family history '{condition}' scored")
            
            # TABLE 8: Sleep Duration
            sleep_duration = user_data.get("sleep_duration")
            if sleep_duration and sleep_duration in HormoneScoringService.SLEEP_DURATION_SCORES:
                HormoneScoringService._add_scores(
                    scores, 
                    HormoneScoringService.SLEEP_DURATION_SCORES[sleep_duration]
                )
                total_signals += 1
                logger.debug(f"Sleep duration '{sleep_duration}' scored")
            
            # TABLE 9: Stress Level
            stress_level = user_data.get("stress_level")
            if stress_level and stress_level in HormoneScoringService.STRESS_LEVEL_SCORES:
                HormoneScoringService._add_scores(
                    scores, 
                    HormoneScoringService.STRESS_LEVEL_SCORES[stress_level]
                )
                total_signals += 1
                logger.debug(f"Stress level '{stress_level}' scored")
            
            # TABLE 10: Workout Intensity
            workout_intensity = user_data.get("workout_intensity")
            if workout_intensity and workout_intensity in HormoneScoringService.WORKOUT_INTENSITY_SCORES:
                HormoneScoringService._add_scores(
                    scores, 
                    HormoneScoringService.WORKOUT_INTENSITY_SCORES[workout_intensity]
                )
                total_signals += 1
                logger.debug(f"Workout intensity '{workout_intensity}' scored")
            
            # Cap all scores at 3 (max rating)
            for hormone in scores:
                scores[hormone] = min(scores[hormone], 3)
            
            # Calculate confidence based on number of signals and score distribution
            confidence = HormoneScoringService._calculate_confidence(scores, total_signals)
            
            scores["confidence"] = confidence
            scores["total_signals"] = total_signals
            
            logger.info(f"Hormone scoring completed: {total_signals} signals analyzed, confidence: {confidence}%")
            logger.info(f"Scores: {scores}")
            
            return scores
            
        except Exception as e:
            logger.error(f"Error calculating hormone scores: {str(e)}")
            # Return default scores on error
            return {
                "estrogen_high": 0,
                "estrogen_low": 0,
                "progesterone_low": 0,
                "androgens_high": 0,
                "insulin_high": 0,
                "cortisol_high": 0,
                "cortisol_low": 0,
                "thyroid_low": 0,
                "confidence": 0,
                "total_signals": 0
            }
    
    @staticmethod
    def _add_scores(current_scores: Dict, new_scores: Dict) -> None:
        """Helper: Add new scores to current scores (accumulate)"""
        for hormone, score in new_scores.items():
            current_scores[hormone] = current_scores.get(hormone, 0) + score
    
    @staticmethod
    def _calculate_confidence(scores: Dict, total_signals: int) -> int:
        """
        Calculate confidence percentage (0-100) based on:
        - Number of symptoms analyzed (more = higher confidence)
        - Score distribution (clear winner = higher confidence)
        """
        if total_signals == 0:
            return 0
        
        # Get hormone scores only (exclude confidence/total_signals)
        hormone_scores = {k: v for k, v in scores.items() 
                         if k not in ["confidence", "total_signals"]}
        
        # Find max score
        max_score = max(hormone_scores.values()) if hormone_scores else 0
        
        if max_score == 0:
            return 30  # Low confidence if no symptoms matched
        
        # Base confidence from signal count (0-50 points)
        signal_confidence = min(total_signals * 5, 50)
        
        # Score strength confidence (0-50 points)
        # Higher max score = more confidence
        score_confidence = min(max_score * 15, 50)
        
        total_confidence = signal_confidence + score_confidence
        
        # Cap at 95 (never 100% certain without lab tests)
        return min(total_confidence, 95)
    
    @staticmethod
    def get_top_hormones(scores: Dict, top_n: int = 3) -> List[tuple]:
        """
        Get top N hormones by score.
        
        Args:
            scores: Hormone scores dictionary
            top_n: Number of top hormones to return
            
        Returns:
            List of tuples: [(hormone_name, score), ...]
        """
        # Filter out non-hormone keys
        hormone_scores = {k: v for k, v in scores.items() 
                         if k not in ["confidence", "total_signals"]}
        
        # Sort by score (descending)
        sorted_hormones = sorted(hormone_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Return only hormones with score > 0
        return [(h, s) for h, s in sorted_hormones[:top_n] if s > 0]
