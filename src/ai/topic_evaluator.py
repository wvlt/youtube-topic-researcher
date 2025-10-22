"""
AI-Powered Topic Evaluator
Uses LLMs to evaluate content topics across multiple dimensions
"""

import logging
import os
from typing import Dict, List, Optional, Tuple
import json
import re


logger = logging.getLogger("content_researcher.ai")


class TopicEvaluator:
    """Evaluates topics using AI for multi-dimensional scoring"""
    
    def __init__(self, provider: str = "anthropic", model: str = None, prompts_config: dict = None):
        """
        Initialize topic evaluator
        
        Args:
            provider: AI provider (anthropic or openai)
            model: Model name
            prompts_config: Prompt configuration
        """
        self.provider = provider.lower()
        self.prompts_config = prompts_config or {}
        
        # Initialize AI client
        if self.provider == "anthropic":
            import anthropic
            self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
            self.model = model or os.getenv('AI_MODEL', 'claude-3-5-sonnet-20241022')
        elif self.provider == "openai":
            import openai
            self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            self.model = model or os.getenv('AI_MODEL', 'gpt-4-turbo-preview')
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")
        
        logger.info(f"AI Evaluator initialized with {self.provider}/{self.model}")
    
    def evaluate_topic(self,
                      topic: str,
                      channel_context: dict,
                      trends: List[str] = None,
                      competitors: List[dict] = None) -> Dict:
        """
        Evaluate a topic across multiple dimensions
        
        Args:
            topic: Topic to evaluate
            channel_context: Channel information and context
            trends: Current trending topics
            competitors: Competitor analysis data
            
        Returns:
            Evaluation scores and analysis
        """
        try:
            prompt = self._build_evaluation_prompt(topic, channel_context, trends, competitors)
            
            response_text = self._call_ai(prompt)
            
            # Parse scores from response
            scores = self._parse_evaluation_response(response_text)
            
            # Add raw analysis
            scores['ai_analysis'] = response_text
            scores['topic'] = topic
            
            logger.debug(f"Evaluated topic '{topic}': {scores['total_score']:.0f}/100")
            return scores
        
        except Exception as e:
            logger.error(f"Error evaluating topic '{topic}': {e}")
            return self._default_scores(topic)
    
    def _build_evaluation_prompt(self,
                                 topic: str,
                                 channel_context: dict,
                                 trends: List[str] = None,
                                 competitors: List[dict] = None) -> str:
        """Build evaluation prompt"""
        
        # Ensure channel_context is a dict
        if not isinstance(channel_context, dict):
            channel_context = {}
        
        # Ensure trends is a list
        if trends is None:
            trends = []
        elif not isinstance(trends, list):
            trends = []
        
        # Ensure competitors is a list
        if competitors is None:
            competitors = []
        elif not isinstance(competitors, list):
            competitors = []
        
        prompt = f"""You are a YouTube content strategy expert. Evaluate this content topic for a YouTube channel.

TOPIC: {topic}

CHANNEL CONTEXT:
- Channel: {channel_context.get('channel_title', 'Unknown')}
- Subscribers: {channel_context.get('subscriber_count', 0):,}
- Average Views: {channel_context.get('avg_views', 0):,}
- Niche: {channel_context.get('niche', 'General')}
- Recent Video Themes: {', '.join(channel_context.get('recent_themes', [])[:5])}

{f"CURRENT TRENDS: {', '.join(trends[:10])}" if trends else ""}

{f"TOP COMPETITOR TOPICS: {', '.join([c.get('title', '') for c in competitors[:5]])}" if competitors else ""}

Rate this topic on these 5 dimensions (0-100 scale):

1. IMPORTANCE (0-100): How relevant and important is this to the channel's niche and audience?
   - Consider alignment with channel's existing content
   - Audience interest and demand
   - Strategic fit for channel growth

2. WATCHABILITY (0-100): How likely will people watch and engage with this content?
   - Entertainment value
   - Educational value
   - Curiosity factor
   - Video length appeal

3. MONETIZATION (0-100): What's the revenue potential?
   - CPM potential for the niche
   - Sponsorship opportunities
   - Affiliate marketing potential
   - Product tie-in possibilities
   - Evergreen vs trending value

4. POPULARITY (0-100): How trending and popular is this topic right now?
   - Current search volume
   - Social media buzz
   - Seasonal relevance
   - Growth trajectory

5. INNOVATION (0-100): How unique and cutting-edge is this angle?
   - Uniqueness of approach
   - State-of-the-art appeal
   - Differentiation from competitors
   - Fresh perspective potential

Provide your response in this EXACT format:

IMPORTANCE: [score]/100
[2-3 sentence justification]

WATCHABILITY: [score]/100
[2-3 sentence justification]

MONETIZATION: [score]/100
[2-3 sentence justification]

POPULARITY: [score]/100
[2-3 sentence justification]

INNOVATION: [score]/100
[2-3 sentence justification]

RECOMMENDED ANGLE: [Your recommended angle or hook for this topic]

KEYWORDS: [5-7 relevant keywords, comma-separated]

COMPETITION LEVEL: [Low/Medium/High]

NOTES: [Any additional strategic insights]"""
        
        return prompt
    
    def _call_ai(self, prompt: str, temperature: float = 0.7) -> str:
        """Call AI API"""
        try:
            if self.provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=2000,
                    temperature=temperature,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            
            elif self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=2000
                )
                return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"AI API call failed: {e}")
            raise
    
    def _parse_evaluation_response(self, response: str) -> Dict:
        """Parse AI evaluation response"""
        scores = {
            'importance_score': 0,
            'watchability_score': 0,
            'monetization_score': 0,
            'popularity_score': 0,
            'innovation_score': 0,
            'total_score': 0,
            'recommended_angle': '',
            'keywords': [],
            'competition_level': 'Medium',
            'notes': ''
        }
        
        try:
            # Extract scores using regex
            importance_match = re.search(r'IMPORTANCE:\s*(\d+)', response, re.IGNORECASE)
            watchability_match = re.search(r'WATCHABILITY:\s*(\d+)', response, re.IGNORECASE)
            monetization_match = re.search(r'MONETIZATION:\s*(\d+)', response, re.IGNORECASE)
            popularity_match = re.search(r'POPULARITY:\s*(\d+)', response, re.IGNORECASE)
            innovation_match = re.search(r'INNOVATION:\s*(\d+)', response, re.IGNORECASE)
            
            if importance_match:
                scores['importance_score'] = float(importance_match.group(1))
            if watchability_match:
                scores['watchability_score'] = float(watchability_match.group(1))
            if monetization_match:
                scores['monetization_score'] = float(monetization_match.group(1))
            if popularity_match:
                scores['popularity_score'] = float(popularity_match.group(1))
            if innovation_match:
                scores['innovation_score'] = float(innovation_match.group(1))
            
            # Calculate total score (weighted average)
            weights = {
                'importance': 0.25,
                'watchability': 0.20,
                'monetization': 0.20,
                'popularity': 0.20,
                'innovation': 0.15
            }
            
            scores['total_score'] = (
                scores['importance_score'] * weights['importance'] +
                scores['watchability_score'] * weights['watchability'] +
                scores['monetization_score'] * weights['monetization'] +
                scores['popularity_score'] * weights['popularity'] +
                scores['innovation_score'] * weights['innovation']
            )
            
            # Extract other information
            angle_match = re.search(r'RECOMMENDED ANGLE:\s*(.+?)(?:\n|$)', response, re.IGNORECASE)
            if angle_match:
                scores['recommended_angle'] = angle_match.group(1).strip()
            
            keywords_match = re.search(r'KEYWORDS:\s*(.+?)(?:\n|$)', response, re.IGNORECASE)
            if keywords_match:
                keywords_str = keywords_match.group(1).strip()
                scores['keywords'] = [k.strip() for k in keywords_str.split(',')]
            
            competition_match = re.search(r'COMPETITION LEVEL:\s*(\w+)', response, re.IGNORECASE)
            if competition_match:
                scores['competition_level'] = competition_match.group(1).strip()
            
            notes_match = re.search(r'NOTES:\s*(.+?)(?:\n\n|$)', response, re.IGNORECASE | re.DOTALL)
            if notes_match:
                scores['notes'] = notes_match.group(1).strip()
        
        except Exception as e:
            logger.error(f"Error parsing evaluation response: {e}")
        
        return scores
    
    def _default_scores(self, topic: str) -> Dict:
        """Return default scores if evaluation fails"""
        return {
            'topic': topic,
            'importance_score': 50,
            'watchability_score': 50,
            'monetization_score': 50,
            'popularity_score': 50,
            'innovation_score': 50,
            'total_score': 50,
            'recommended_angle': 'Standard approach',
            'keywords': [],
            'competition_level': 'Medium',
            'notes': 'Evaluation failed - using default scores',
            'ai_analysis': ''
        }
    
    def batch_evaluate_topics(self,
                             topics: List[str],
                             channel_context: dict,
                             trends: List[str] = None,
                             competitors: List[dict] = None) -> List[Dict]:
        """
        Evaluate multiple topics
        
        Args:
            topics: List of topics to evaluate
            channel_context: Channel information
            trends: Current trends
            competitors: Competitor data
            
        Returns:
            List of evaluation results
        """
        results = []
        
        for i, topic in enumerate(topics):
            logger.info(f"Evaluating topic {i+1}/{len(topics)}: {topic}")
            
            evaluation = self.evaluate_topic(
                topic=topic,
                channel_context=channel_context,
                trends=trends,
                competitors=competitors
            )
            
            results.append(evaluation)
        
        # Sort by total score
        results.sort(key=lambda x: x['total_score'], reverse=True)
        
        return results
    
    def generate_topic_ideas(self,
                            channel_context: dict,
                            count: int = 10,
                            trends: List[str] = None) -> List[str]:
        """
        Generate topic ideas using AI
        
        Args:
            channel_context: Channel information
            count: Number of topics to generate
            trends: Current trends
            
        Returns:
            List of topic ideas
        """
        try:
            prompt = f"""You are a YouTube content strategist. Generate {count} high-potential video topic ideas for this channel:

CHANNEL: {channel_context.get('channel_title', 'Unknown')}
NICHE: {channel_context.get('niche', 'General')}
SUBSCRIBERS: {channel_context.get('subscriber_count', 0):,}
RECENT THEMES: {', '.join(channel_context.get('recent_themes', [])[:10])}

{f"CURRENT TRENDS: {', '.join(trends[:15])}" if trends else ""}

Generate {count} specific, actionable video topics that:
1. Align with the channel's niche and audience
2. Have high watch potential
3. Are monetizable
4. Include trending elements
5. Offer unique angles

Format: One topic per line, numbered.
Make each topic specific and compelling (not generic).

Topics:"""
            
            response = self._call_ai(prompt, temperature=0.8)
            
            # Parse topics from response
            topics = []
            for line in response.split('\n'):
                line = line.strip()
                # Remove numbering
                line = re.sub(r'^\d+[\.\)]\s*', '', line)
                if line and len(line) > 10:
                    topics.append(line)
            
            logger.info(f"Generated {len(topics)} topic ideas")
            return topics[:count]
        
        except Exception as e:
            logger.error(f"Error generating topics: {e}")
            return []

