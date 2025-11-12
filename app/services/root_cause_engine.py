from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class RootCauseEngine:
    """
    Hormone imbalance root cause analysis engine
    Uses clinical scoring tables to analyze symptoms and predict hormone imbalances
    """
    
    @staticmethod
    def analyze_hormone_imbalance(user_data: Dict) -> Dict[str, any]:
        """
        Analyze hormone imbalance based on user data using clinical scoring.
        
        Args:
            user_data: User survey data containing:
                - period_description, cycle_length
                - period_concerns, body_concerns, skin_hair_concerns, mental_health_concerns
                - family_history, sleep_duration, stress_level, workout_intensity
            
        Returns:
            Dict containing:
            - primary_imbalance: Primary hormone imbalance (e.g., "progesterone")
            - primary_level: Primary hormone level (e.g., "low")
            - secondary_imbalances: List of secondary hormone imbalances (e.g., ["testosterone"])
            - secondary_levels: List of secondary hormone levels (e.g., ["low"])
            - hormone_scores: Dict with all 8 hormone scores (0-3)
            - confidence: Confidence percentage (0-100)
        """
        try:
            from app.services.hormone_scoring_service import HormoneScoringService
            
            # Calculate detailed hormone scores (0-3 for each hormone)
            scores = HormoneScoringService.calculate_hormone_scores(user_data)
            
            # Get top 3 hormones by score
            top_hormones = HormoneScoringService.get_top_hormones(scores, top_n=3)
            
            if not top_hormones or top_hormones[0][1] == 0:
                # No clear hormone imbalance detected - return defaults
                logger.warning("No hormone imbalance detected from symptoms")
                return {
                    "primary_imbalance": "progesterone",
                    "primary_level": "low",
                    "secondary_imbalances": [],
                    "secondary_levels": [],
                    "hormone_scores": scores,
                    "confidence": scores.get("confidence", 0)
                }
            
            # Extract primary hormone (highest score)
            primary_hormone_full = top_hormones[0][0]  # e.g., "androgens_high"
            primary_score = top_hormones[0][1]
            
            # Parse hormone name and level
            primary_name, primary_level = RootCauseEngine._parse_hormone_name(primary_hormone_full)
            
            # Extract secondary hormones (2nd and 3rd highest, if score > 0)
            secondary_imbalances = []
            secondary_levels = []
            
            for hormone_full, score in top_hormones[1:]:
                if score > 0:  # Only include if score > 0
                    hormone_name, hormone_level = RootCauseEngine._parse_hormone_name(hormone_full)
                    secondary_imbalances.append(hormone_name)
                    secondary_levels.append(hormone_level)
            
            result = {
                "primary_imbalance": primary_name,
                "primary_level": primary_level,
                "secondary_imbalances": secondary_imbalances,
                "secondary_levels": secondary_levels,
                "hormone_scores": scores,
                "confidence": scores.get("confidence", 0)
            }
            
            logger.info(f"Hormone analysis: Primary={primary_name} ({primary_level}), "
                       f"Secondary={secondary_imbalances}, Confidence={scores.get('confidence', 0)}%")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in hormone analysis: {str(e)}", exc_info=True)
            # Fallback to safe defaults
            return {
                "primary_imbalance": "progesterone",
                "primary_level": "low",
                "secondary_imbalances": [],
                "secondary_levels": [],
                "hormone_scores": {},
                "confidence": 0
            }
    
    @staticmethod
    def _parse_hormone_name(hormone_full: str) -> Tuple[str, str]:
        """
        Parse full hormone name to extract name and level.
        
        Examples:
            "androgens_high" -> ("androgens", "high")
            "progesterone_low" -> ("progesterone", "low")
            "estrogen_high" -> ("estrogen", "high")
            
        Args:
            hormone_full: Full hormone name (e.g., "androgens_high")
            
        Returns:
            Tuple of (hormone_name, level)
        """
        # Split by underscore
        parts = hormone_full.rsplit("_", 1)
        
        if len(parts) == 2:
            hormone_name = parts[0]
            level = parts[1]  # "high" or "low"
        else:
            # Fallback if no underscore found
            hormone_name = hormone_full
            level = "low"
        
        # Map to frontend-expected names
        # Frontend uses: "progesterone", "testosterone", "estrogen", etc.
        name_mapping = {
            "androgens": "testosterone",  # Frontend shows "testosterone" for androgens
            "progesterone": "progesterone",
            "estrogen": "estrogen",
            "insulin": "insulin",
            "cortisol": "cortisol",
            "thyroid": "thyroid"
        }
        
        frontend_name = name_mapping.get(hormone_name, hormone_name)
        
        return (frontend_name, level)
    
    @staticmethod
    def get_formatted_imbalance_text(analysis_result: Dict) -> str:
        """
        Format analysis result into text for prompts
        
        Args:
            analysis_result: Result from analyze_hormone_imbalance
            
        Returns:
            Formatted text (e.g., "progesterone (low), Secondary: testosterone (low)")
        """
        primary = f"{analysis_result['primary_imbalance']} ({analysis_result['primary_level']})"
        
        if analysis_result['secondary_imbalances']:
            secondary_parts = []
            for i, hormone in enumerate(analysis_result['secondary_imbalances']):
                level = analysis_result['secondary_levels'][i] if i < len(analysis_result['secondary_levels']) else "unknown"
                secondary_parts.append(f"{hormone} ({level})")
            secondary_text = f", Secondary: {', '.join(secondary_parts)}"
        else:
            secondary_text = ""
            
        return f"{primary}{secondary_text}"
    
    @staticmethod
    def get_related_hormones(analysis_result: Dict) -> List[str]:
        """
        Extract related hormones from analysis result
        
        Args:
            analysis_result: Result from analyze_hormone_imbalance
            
        Returns:
            List of related hormones (e.g., ["progesterone", "testosterone"])
        """
        hormones = [analysis_result['primary_imbalance']]
        hormones.extend(analysis_result['secondary_imbalances'])
        return hormones
