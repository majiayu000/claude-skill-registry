### /mnt/data2/nhlstats/.github/skills/elo-rating-systems/SKILL.md
```markdown
1: ---
2: name: elo-rating-systems
3: description: Explains the implementation of Elo rating systems, including the unified BaseEloRating interface, core formulas, sport-specific parameters (K-factor, home advantage), and update logic.
4: version: 2.1.0
5: ---
6:
7: # Elo Rating Systems
8:
9: ## ✅ Unified Interface (BaseEloRating) - COMPLETED

**Status**: All 9 sport-specific Elo implementations have been successfully refactored to inherit from `BaseEloRating`.
10:
11: All sport-specific Elo implementations now inherit from `BaseEloRating` (located in `plugins/elo/base_elo_rating.py`). This provides a consistent interface across all sports.
12:
13: ### BaseEloRating Abstract Class
14:
15: ```python
16: from abc import ABC, abstractmethod
17: from typing import Dict, Optional, Union
18:
19: class BaseEloRating(ABC):
20:     """
21:     Abstract base class for Elo rating systems.
22:
23:     This defines the common interface that all sport-specific Elo implementations
24:     must follow to ensure consistency across the betting system.
25:     """
26:
27:     def __init__(
28:         self,
29:         k_factor: float = 32.0,
30:         home_advantage: float = 100.0,
31:         initial_rating: float = 1500.0
32:     ):
33:         self.k_factor = k_factor
34:         self.home_advantage = home_advantage
35:         self.initial_rating = initial_rating
36:         self.ratings: Dict[str, float] = {}
37:
38:     @abstractmethod
39:     def predict(self, home_team: str, away_team: str, is_neutral: bool = False) -> float:
40:         """
41:         Predict probability of home team winning.
42:
43:         Args:
44:             home_team: Name of home team
45:             away_team: Name of away team
46:             is_neutral: Whether the game is at a neutral site (no home advantage)
47:
48:         Returns:
49:             float: Probability of home win (0.0 to 1.0)
50:         """
51:         pass
52:
53:     @abstractmethod
54:     def update(
55:         self,
56:         home_team: str,
57:         away_team: str,
58:         home_won: Union[bool, float],
59:         is_neutral: bool = False
60:     ) -> None:
61:         """
62:         Update Elo ratings after a game result.
63:
64:         Args:
65:             home_team: Name of home team
66:             away_team: Name of away team
67:             home_won: Whether home team won (True/False) or score margin (float)
68:             is_neutral: Whether the game was at a neutral site
69:         """
70:         pass
71:
72:     @abstractmethod
73:     def get_rating(self, team: str) -> float:
74:         """
75:         Get current Elo rating for a team.
76:
77:         Args:
78:             team: Name of team
79:
80:         Returns:
81:             float: Current Elo rating
82:         """
83:         pass
84:
85:     @abstractmethod
86:     def expected_score(self, rating_a: float, rating_b: float) -> float:
87:         """
88:         Calculate expected score (probability of team A winning).
89:
90:         Uses standard Elo formula:
91:         E_A = 1 / (1 + 10^((R_B - R_A) / 400))
92:
93:         Args:
94:             rating_a: Rating of team A
95:             rating_b: Rating of team B
96:
97:         Returns:
98:             float: Probability of team A winning (0.0 to 1.0)
99:         """
100:         pass
101:
102:     @abstractmethod
103:     def get_all_ratings(self) -> Dict[str, float]:
104:         """
105:         Get all current ratings.
106:
107:         Returns:
108:             Dict[str, float]: Copy of all team ratings
109:         """
110:         pass
111:
112:     def _apply_home_advantage(self, home_rating: float, is_neutral: bool = False) -> float:
113:         """
114:         Apply home advantage adjustment to rating.
115:
116:         Args:
117:             home_rating: Base home team rating
118:             is_neutral: Whether game is at neutral site
119:
120:         Returns:
121:             float: Adjusted home rating
122:         """
123:         if is_neutral:
124:             return home_rating
125:         return home_rating + self.home_advantage
126:
127:     def _calculate_rating_change(
128:         self,
129:         actual: float,
130:         expected: float,
131:         k_factor: Optional[float] = None
132:     ) -> float:
133:         """
134:         Calculate rating change using Elo formula.
135:
136:         Args:
137:             actual: Actual result (1 for win, 0 for loss, or margin)
138:             expected: Expected probability of winning
139:             k_factor: Optional custom k-factor (uses self.k_factor if None)
140:
141:         Returns:
142:             float: Rating change (positive if actual > expected)
143:         """
144:         if k_factor is None:
145:             k_factor = self.k_factor
146:         return k_factor * (actual - expected)
147: ```
148:
149: ## Core Formula
150:
151: Convert Elo ratings to win probability:
152:
153: ```python
154: def expected_score(rating_a: float, rating_b: float) -> float:
155:     """Probability that team A beats team B."""
156:     return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
157: ```
158:
159: For home games, add home advantage to home team's rating before calculation (handled by `_apply_home_advantage()`).
160:
161: ## Sport-Specific Parameters
162:
163: | Sport | K-Factor | Home Advantage | Notes | Refactoring Status |
164: |-------|----------|----------------|-------|-------------------|
165: | NBA   | 20       | 100            | High-scoring, consistent | ✅ COMPLETED |
166: | NHL   | 20       | 100            | High variance, recency weighting | ✅ COMPLETED |
167: | MLB   | 20       | 50             | Lower home advantage | ✅ COMPLETED |
168: | NFL   | 20       | 65             | Small sample sizes | ✅ COMPLETED |
169: | EPL   | 20       | 60             | 3-way outcomes (Home/Draw/Away) | ✅ COMPLETED |
170: | Ligue1| 20       | 60             | 3-way outcomes (Home/Draw/Away) | ✅ COMPLETED |
171: | NCAAB | 20       | 100            | College basketball | 🔄 IN PROGRESS |
172: | WNCAAB| 20       | 100            | Women's college basketball | 🔄 IN PROGRESS |
173: | Tennis| 20       | 0              | No home advantage | 🔄 IN PROGRESS |
174:
175: ## Implementation Requirements
176:
177: ### For New Sport Implementations
178:
179: 1. **Inherit from BaseEloRating**:
180:    ```python
181:    from .base_elo_rating import BaseEloRating
182:
183:    class NewSportEloRating(BaseEloRating):
184:    ```
185:
186: 2. **Implement all abstract methods**:
187:    - `predict()` - Must accept `is_neutral` parameter
188:    - `update()` - Must accept `home_won: Union[bool, float]` and `is_neutral` parameters
189:    - `get_rating()` - Return current rating, initialize if needed
190:    - `expected_score()` - Standard Elo formula
191:    - `get_all_ratings()` - Return copy of ratings dictionary
192:
193: 3. **Call super().__init__()**:
194:    ```python
195:    def __init__(self, k_factor: float = 20.0, home_advantage: float = 100.0, initial_rating: float = 1500.0):
196:        super().__init__(k_factor=k_factor, home_advantage=home_advantage, initial_rating=initial_rating)
197:    ```
198:
199: ### For Refactoring Existing Sport Classes
200:
201: 1. **Create TDD tests first**:
202:    - Test inheritance from BaseEloRating
203:    - Test all required methods exist
204:    - Test backward compatibility
205:
206: 2. **Update class definition**:
207:    ```python
208:    class ExistingSportEloRating(BaseEloRating):  # Changed from standalone class
209:    ```
210:
211: 3. **Add missing methods**:
212:    - Most classes need `get_all_ratings()`
213:    - Some need `expected_score()`
214:    - Update method signatures to match base interface
215:
216: 4. **Add backward compatibility methods**:
217:    ```python
218:    def legacy_update(self, home_team: str, away_team: str, result: Union[str, int]) -> float:
219:        """Legacy update method for backward compatibility."""
220:        # Convert legacy result format to home_won
221:        # Call self.update() with converted parameters
222:    ```
223:
224: ## Sport-Specific Features
225:
226: ### Soccer (EPL, Ligue1)
227: - **3-way outcomes**: Home win, Draw, Away win
228: - **Draw probability modeling**: Gaussian distribution based on rating difference
229: - **Methods**: `predict_3way()`, `predict_probs()` for backward compatibility
230:
231: ### NHL
232: - **Recency weighting**: More recent games have greater impact
233: - **Game history tracking**: `game_history` dictionary
234: - **Season reversion**: `apply_season_reversion()` method
235:
236: ### MLB, NFL
237: - **Score-based updates**: `update_with_scores()` or `update_legacy()` methods
238: - **Margin of victory**: Score differences affect rating changes
239:
240: ## Testing Elo Implementations
241:
242: ### TDD Test Pattern
243: ```python
244: import pytest
245: from plugins.elo import BaseEloRating, SportEloRating
246:
247: class TestSportEloRatingTDD:
248:     def test_inherits_from_base(self):
249:         """Test that SportEloRating inherits from BaseEloRating."""
250:         assert issubclass(SportEloRating, BaseEloRating)
251:
252:     def test_has_required_methods(self):
253:         """Test that SportEloRating implements all abstract methods."""
254:         elo = SportEloRating()
255:         assert hasattr(elo, 'predict')
256:         assert hasattr(elo, 'update')
257:         assert hasattr(elo, 'get_rating')
258:         assert hasattr(elo, 'expected_score')
259:         assert hasattr(elo, 'get_all_ratings')
260:
261:     def test_backward_compatibility(self):
262:         """Test backward compatibility with existing functionality."""
263:         elo = SportEloRating()
264:         # Test that sport-specific features still work
265: ```
266:
267: ### Tennis Adaptation

The `TennisEloRating` class required special adaptation due to its different interface:

**Key Differences from Team Sports**:
1. **Player-based vs Team-based**: Uses `player_a`/`player_b` instead of `home_team`/`away_team`
2. **No Home Advantage**: Tennis is always neutral (`home_advantage=0`)
3. **Tour Separation**: Maintains separate ratings for ATP and WTA tours
4. **Name Normalization**: Converts names to "Lastname F." format (e.g., "Novak Djokovic" → "Djokovic N.")
5. **Match Tracking**: Tracks match counts for dynamic K-factor adjustments

**Interface Bridge Methods**:
- `predict_team()`: Adapts team-based predict to tennis player-based predict
- `update_team()`: Adapts team-based update to tennis player-based update
- These methods allow TennisEloRating to satisfy the BaseEloRating interface while maintaining tennis-specific functionality

### Import Pattern
268: ```python
269: # Import from unified elo package
270: from plugins.elo import BaseEloRating, NHLEloRating, NBAEloRating, MLBEloRating, NFLEloRating
271: from plugins.elo import EPLEloRating, Ligue1EloRating, NCAABEloRating, WNCAABEloRating, TennisEloRating
272: ```
273:
274: ## Threshold Tuning
275:
276: Use lift/gain analysis to optimize thresholds:
277:
278: ```python
279: from lift_gain_analysis import analyze_sport
280:
281: # Analyze prediction quality by decile
282: overall, current_season = analyze_sport('nba')
283:
284: # Look for deciles with lift > 1.2
285: # Set threshold to capture high-lift predictions
286: ```
287:
288: **Key metrics:**
289: - **Lift > 1.0**: Predictions better than random
290: - **Target**: Find threshold where top deciles have lift > 1.3
291:
292: ## Files to Reference
293:
294: - `plugins/elo/base_elo_rating.py` - Unified base class
295: - `plugins/elo/nba_elo_rating.py` - Canonical implementation
296: - `plugins/elo/nhl_elo_rating.py` - NHL with recency weighting
297: - `plugins/elo/epl_elo_rating.py` - Soccer with 3-way outcomes
298: - `plugins/lift_gain_analysis.py` - Threshold analysis
299: - `tests/test_base_elo_rating_tdd.py` - Base class tests
300: - `tests/test_*_elo_tdd.py` - Sport-specific TDD tests
301:
302: ## Current Status (2026-01-23)
303:
304: **Refactoring Progress:** 6/9 sports completed
305: - ✅ **Completed**: NHL, NBA, MLB, NFL, EPL, Ligue1
306: - 🔄 **In Progress**: NCAAB, WNCAAB, Tennis
307: - 📋 **Pending**: Update SPORTS_CONFIG, DAGs, and dashboard to use unified interface
308:
309: **Key Changes:**
310: 1. All Elo code moved to `plugins/elo/` directory
311: 2. `BaseEloRating` abstract class defines unified interface
312: 3. Sport classes maintain backward compatibility with `legacy_update()` methods
313: 4. TDD approach used for all refactoring
```
