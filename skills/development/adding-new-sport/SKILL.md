### /mnt/data2/nhlstats/.github/skills/adding-new-sport/SKILL.md
```markdown
1: ---
2: name: adding-new-sport
3: description: Instructions and checklist for integrating a new sport into the betting system, including unified Elo ratings (inheriting from BaseEloRating), game downloading, and DAG configuration.
4: version: 2.1.0
5: ---
6:
7: # Adding a New Sport
8:
9: ## Overview

**Status**: The unified Elo rating interface (`BaseEloRating`) is now **COMPLETED** and ready for new sports. All 9 existing sports have been successfully refactored to use this interface.
10:
11: This guide explains how to add a new sport to the multi-sport betting system. All new sport Elo implementations must inherit from the unified `BaseEloRating` interface.
12:
13: ## Required Files
14:
15: ### 1. Elo Rating Module (Unified Interface)
16: **Location:** `plugins/elo/{sport}_elo_rating.py`
17:
18: ```python
19: """
20: {Sport} Elo Rating System.
21:
22: Production-ready Elo rating system for {Sport} predictions.
23: Inherits from BaseEloRating for unified interface.
24: """
25:
26: from typing import Dict, Union
27: from .base_elo_rating import BaseEloRating
28:
29:
30: class {Sport}EloRating(BaseEloRating):
31:     """
32:     {Sport}-specific Elo rating system.
33:
34:     Inherits from BaseEloRating for unified interface.
35:     """
36:
37:     def __init__(self, k_factor: float = 20.0, home_advantage: float = 100.0, initial_rating: float = 1500.0):
38:         """
39:         Initialize {Sport} Elo rating system.
40:
41:         Args:
42:             k_factor: How quickly ratings change (20 is standard)
43:             home_advantage: Elo points added for home field
44:             initial_rating: Starting rating for new teams (1500 is standard)
45:         """
46:         super().__init__(k_factor=k_factor, home_advantage=home_advantage, initial_rating=initial_rating)
47:
48:     def predict(self, home_team: str, away_team: str, is_neutral: bool = False) -> float:
49:         """
50:         Predict probability of home team winning.
51:
52:         Args:
53:             home_team: Name of home team
54:             away_team: Name of away team
55:             is_neutral: Whether the game is at a neutral site (no home advantage)
56:
57:         Returns:
58:             float: Probability of home win (0.0 to 1.0)
59:         """
60:         # Get base ratings
61:         rh = self.get_rating(home_team)
62:         ra = self.get_rating(away_team)
63:
64:         # Apply home advantage if not neutral
65:         if not is_neutral:
66:             rh = self._apply_home_advantage(rh, is_neutral=False)
67:
68:         # Calculate expected score
69:         return self.expected_score(rh, ra)
70:
71:     def update(
72:         self,
73:         home_team: str,
74:         away_team: str,
75:         home_won: Union[bool, float],
76:         is_neutral: bool = False
77:     ) -> None:
78:         """
79:         Update Elo ratings after a game result.
80:
81:         Args:
82:             home_team: Name of home team
83:             away_team: Name of away team
84:             home_won: Whether home team won (True/False) or score margin (float)
85:             is_neutral: Whether the game was at a neutral site
86:         """
87:         # Get current ratings
88:         rh = self.get_rating(home_team)
89:         ra = self.get_rating(away_team)
90:
91:         # Apply home advantage if not neutral
92:         home_rating = rh
93:         if not is_neutral:
94:             home_rating = self._apply_home_advantage(rh, is_neutral=False)
95:
96:         # Calculate expected score for home team
97:         expected_home = self.expected_score(home_rating, ra)
98:
99:         # Determine actual score based on home_won
100:         if isinstance(home_won, bool):
101:             actual_home = 1.0 if home_won else 0.0
102:         else:
103:             # For score margin, use appropriate transformation
104:             # Example: logistic transformation for margin effects
105:             actual_home = 1.0 / (1.0 + math.exp(-home_won))
106:
107:         # Calculate rating changes
108:         home_change = self._calculate_rating_change(actual_home, expected_home)
109:
110:         # Update ratings (conservation of points)
111:         self.ratings[home_team] = rh + home_change
112:         self.ratings[away_team] = ra - home_change
113:
114:     def get_rating(self, team: str) -> float:
115:         """
116:         Get current Elo rating for a team.
117:
118:         Args:
119:             team: Name of team
120:
121:         Returns:
122:             float: Current Elo rating
123:         """
124:         if team not in self.ratings:
125:             self.ratings[team] = self.initial_rating
126:         return self.ratings[team]
127:
128:     def expected_score(self, rating_a: float, rating_b: float) -> float:
129:         """
130:         Calculate expected score (probability of team A winning).
131:
132:         Uses standard Elo formula:
133:         E_A = 1 / (1 + 10^((R_B - R_A) / 400))
134:
135:         Args:
136:             rating_a: Rating of team A
137:             rating_b: Rating of team B
138:
139:         Returns:
140:             float: Probability of team A winning (0.0 to 1.0)
141:         """
142:         return 1.0 / (1.0 + 10.0 ** ((rating_b - rating_a) / 400.0))
143:
144:     def get_all_ratings(self) -> Dict[str, float]:
145:         """
146:         Get all current ratings.
147:
148:         Returns:
149:             Dict[str, float]: Copy of all team ratings
150:         """
151:         return self.ratings.copy()
152:
153:     # Optional: Add sport-specific methods
154:     # def sport_specific_method(self, ...):
155:     #     """Sport-specific functionality."""
156: ```
157:
158: **Key Requirements:**
159: 1. Must inherit from `BaseEloRating`
160: 2. Must implement all 5 abstract methods
161: 3. Must call `super().__init__()` in constructor
162: 4. Should use `_apply_home_advantage()` and `_calculate_rating_change()` helper methods
163:
164: ### 2. Games Downloader
165: **Location:** `plugins/{sport}_games.py`
166:
167: ```python
168: """
169: {Sport} game data downloader.
170:
171: Downloads game data from official API and loads into database.
172: """
173:
174: import pandas as pd
175: from typing import List, Dict
176: from datetime import datetime
177:
178: def download_{sport}_games(date: str = None) -> List[Dict]:
179:     """
180:     Download {sport} games from API.
181:
182:     Args:
183:         date: Optional date string (YYYY-MM-DD) to filter games
184:
185:     Returns:
186:         List of game dictionaries with standardized format
187:     """
188:     # Fetch from official API
189:     # Parse into standard format
190:     games = []
191:
192:     # Standard game format:
193:     # {
194:     #     'game_id': '{SPORT}_{YYYYMMDD}_{HOME}_{AWAY}',
195:     #     'sport': '{sport}',
196:     #     'date': 'YYYY-MM-DD',
197:     #     'home_team': 'Home Team Name',
198:     #     'away_team': 'Away Team Name',
199:     #     'home_score': int,
200:     #     'away_score': int,
201:     #     'result': 'H'/'A'/'D' (or appropriate for sport)
202:     # }
203:
204:     return games
205:
206: def load_{sport}_games_to_db(games: List[Dict]):
207:     """
208:     Load games into unified_games table.
209:
210:     Args:
211:         games: List of game dictionaries
212:     """
213:     from db_manager import default_db
214:
215:     if not games:
216:         return
217:
218:     # Convert to DataFrame
219:     df = pd.DataFrame(games)
220:
221:     # Ensure proper column types
222:     # Insert into database
223:     default_db.insert_df('unified_games', df, if_exists='append')
224:
225:     print(f"✓ Loaded {len(games)} {sport} games to database")
226: ```
227:
228: ### 3. Update Elo Package Exports
229: **Location:** `plugins/elo/__init__.py`
230:
231: Add import to the `__init__.py` file:
232:
233: ```python
234: # ... existing imports
235: from .{sport}_elo_rating import {Sport}EloRating
236:
237: __all__ = [
238:     # ... existing exports
239:     '{Sport}EloRating',
240: ]
241: ```
242:
243: ### 4. DAG Configuration
244: Add to `SPORTS_CONFIG` in `dags/multi_sport_betting_workflow.py`:
245:
246: ```python
247: SPORTS_CONFIG = {
248:     # ... existing sports
249:     "{sport}": {
250:         "elo_class": "{Sport}EloRating",  # Class name (not module)
251:         "games_module": "{sport}_games",
252:         "kalshi_function": "fetch_{sport}_markets",
253:         "elo_threshold": 0.70,  # Tune with lift/gain analysis
254:         "k_factor": 20.0,  # Sport-specific parameters
255:         "home_advantage": 100.0,
256:     },
257: }
258: ```
259:
260: ### 5. Kalshi Market Function
261: Add to `plugins/kalshi_markets.py`:
262:
263: ```python
264: def fetch_{sport}_markets() -> List[Dict]:
265:     """
266:     Fetch {SPORT} markets from Kalshi.
267:
268:     Returns:
269:         List of market dictionaries
270:     """
271:     markets = []
272:
273:     try:
274:         # Example for Kalshi API
275:         response = kalshi_client.get_markets(
276:             series_ticker="{SPORT}WIN",  # Adjust based on sport
277:             status="open",
278:             limit=100
279:         )
280:
281:         markets = response.get("markets", [])
282:
283:     except Exception as e:
284:         print(f"⚠️ Failed to fetch {sport} markets: {e}")
285:
286:     return markets
287: ```
288:
289: ### 6. Team Name Mappings
290: Update `plugins/naming_resolver.py`:
291:
292: ```python
293: # Add to TEAM_MAPPINGS dictionary
294: TEAM_MAPPINGS.update({
295:     "{sport}": {
296:         "API_TEAM_NAME": "DISPLAY_TEAM_NAME",
297:         # ... all teams for this sport
298:     }
299: })
300: ```
301:
302: ## Game ID Format
303:
304: Consistent format: `{SPORT}_{YYYYMMDD}_{HOME}_{AWAY}`
305:
306: ```python
307: def generate_game_id(sport: str, date: str, home: str, away: str) -> str:
308:     """
309:     Generate consistent game ID.
310:
311:     Args:
312:         sport: Sport abbreviation (lowercase)
313:         date: Date string (YYYY-MM-DD)
314:         home: Home team name
315:         away: Away team name
316:
317:     Returns:
318:         Game ID string
319:     """
320:     date_str = date.replace('-', '')
321:     home_slug = "".join(filter(str.isalnum, home)).upper()
322:     away_slug = "".join(filter(str.isalnum, away)).upper()
323:     return f"{sport.upper()}_{date_str}_{home_slug}_{away_slug}"
324: ```
325:
326: ## TDD Approach for New Sport
327:
328: ### 1. Create TDD Test File
329: **Location:** `tests/test_{sport}_elo_tdd.py`
330:
331: ```python
332: """
333: Test suite for {Sport}EloRating using TDD approach.
334: Tests the new {Sport}EloRating that inherits from BaseEloRating.
335: """
336:
337: import pytest
338: import sys
339: import os
340: sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
341:
342: from plugins.elo import BaseEloRating, {Sport}EloRating
343:
344:
345: class Test{Sport}EloRatingTDD:
346:     """Test {Sport}EloRating implementation using TDD."""
347:
348:     def test_{sport}_elo_inherits_from_base(self):
349:         """Test that {Sport}EloRating inherits from BaseEloRating."""
350:         assert issubclass({Sport}EloRating, BaseEloRating)
351:
352:     def test_{sport}_elo_has_required_methods(self):
353:         """Test that {Sport}EloRating implements all abstract methods."""
354:         elo = {Sport}EloRating()
355:
356:         # Check all abstract methods exist
357:         assert hasattr(elo, 'predict')
358:         assert hasattr(elo, 'update')
359:         assert hasattr(elo, 'get_rating')
360:         assert hasattr(elo, 'expected_score')
361:         assert hasattr(elo, 'get_all_ratings')
362:
363:     def test_{sport}_elo_basic_functionality(self):
364:         """Test basic Elo functionality."""
365:         elo = {Sport}EloRating(k_factor=20, home_advantage=100, initial_rating=1500)
366:
367:         # Test rating initialization
368:         assert elo.get_rating("TeamA") == 1500
369:         assert elo.get_rating("TeamB") == 1500
370:
371:         # Test prediction
372:         prob = elo.predict("TeamA", "TeamB")
373:         assert 0 <= prob <= 1
374:
375:         # Test update
376:         initial_rating = elo.get_rating("TeamA")
377:         elo.update("TeamA", "TeamB", home_won=True)
378:         new_rating = elo.get_rating("TeamA")
379:         assert new_rating > initial_rating
380:
381:     def test_{sport}_elo_get_all_ratings(self):
382:         """Test get_all_ratings method."""
383:         elo = {Sport}EloRating()
384:
385:         # Add some ratings
386:         elo.update("TeamA", "TeamB", home_won=True)
387:         elo.update("TeamC", "TeamD", home_won=False)
388:
389:         all_ratings = elo.get_all_ratings()
390:
391:         assert isinstance(all_ratings, dict)
392:         assert "TeamA" in all_ratings
393:         assert "TeamB" in all_ratings
394:         assert "TeamC" in all_ratings
395:         assert "TeamD" in all_ratings
396:         assert len(all_ratings) == 4
397:
398:
399: if __name__ == "__main__":
400:     pytest.main([__file__, "-v"])
401: ```
402:
403: ### 2. Run TDD Cycle
404: 1. **Red**: Run tests - they should fail (class doesn't exist yet)
405: 2. **Green**: Create the Elo class with minimal implementation
406: 3. **Refactor**: Add proper type hints, docstrings, error handling
407: 4. **Test**: Ensure all tests pass
408:
409: ## Validation Checklist
410:
411: - [ ] Elo class inherits from `BaseEloRating`
412: - [ ] All 5 abstract methods implemented
413: - [ ] Games download returns proper format
414: - [ ] Team names resolve correctly in naming resolver
415: - [ ] Kalshi markets parse properly
416: - [ ] Data loads to database without errors
417: - [ ] TDD tests pass with 100% coverage for Elo class
418: - [ ] DAG parses without errors
419: - [ ] Added to `plugins/elo/__init__.py` exports
420: - [ ] Updated `SPORTS_CONFIG` in DAG
421:
422: ## Testing
423:
424: ```bash
425: # Test DAG parsing
426: python dags/multi_sport_betting_workflow.py
427:
428: # Run sport-specific TDD tests
429: pytest tests/test_{sport}_elo_tdd.py -v
430:
431: # Check coverage for new Elo class
432: pytest --cov=plugins/elo/{sport}_elo_rating.py --cov-report=term-missing
433:
434: # Validate data integration
435: python -c "from data_validation import validate_{sport}_data; validate_{sport}_data().print_report()"
436: ```
437:
438: ## Files to Reference
439:
440: - `plugins/elo/base_elo_rating.py` - Unified base class interface
441: - `plugins/elo/nba_elo_rating.py` - Template for Elo implementation
442: - `plugins/nba_games.py` - Template for games downloader
443: - `plugins/kalshi_markets.py` - Add Kalshi function here
444: - `tests/test_nba_elo_tdd.py` - Template for TDD tests
445:
446: ## Sport-Specific Considerations
447:
448: ### For Sports with Draws (Soccer)
449: - Implement `predict_3way()` and `predict_probs()` methods
450: - Add `legacy_update()` method for backward compatibility with 3-way outcomes
451: - Model draw probability based on rating difference
452:
453: ### For Score-Based Sports (MLB, NFL)
454: - Implement `update_with_scores()` method
455: - Consider margin of victory in rating changes
456: - Add `update_legacy()` method for backward compatibility
457:
458: ### For Individual Sports (Tennis)
459: - Set `home_advantage=0` (no home advantage)
460: - Consider surface-specific adjustments if needed
461:
462: ## Current Sport Implementations (Reference)
463:
464: **Successfully implemented:**
465: - `NHLEloRating` - NHL with recency weighting
466: - `NBAEloRating` - Canonical implementation
467: - `MLBEloRating` - MLB with score-based updates
468: - `NFLEloRating` - NFL with score-based updates
469: - `EPLEloRating` - EPL with 3-way outcomes
470: - `Ligue1EloRating` - Ligue1 with 3-way outcomes
471:
472: **In progress:**
473: - `NCAABEloRating` - College basketball
474: - `WNCAABEloRating` - Women's college basketball
475: - `TennisEloRating` - Tennis (no home advantage)
```
