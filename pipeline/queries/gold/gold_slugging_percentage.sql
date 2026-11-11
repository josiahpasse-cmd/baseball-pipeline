SELECT 
    g.Season,
    'MLB Overall' AS League,
    SUM(b.Hits - b.Doubles - b.Triples - b.HomeRuns) AS Singles,
    SUM(b.Doubles) AS Doubles,
    SUM(b.Triples) AS Triples,
    SUM(b.HomeRuns) AS Homeruns,
    SUM(b.AtBats) AS AtBats,
    ROUND(((SUM(b.Hits) - SUM(b.Doubles) - SUM(b.Triples) - SUM(b.HomeRuns)) + (SUM(b.Doubles) * 2) + (SUM(b.Triples) * 3) + (SUM(b.HomeRuns) * 4)) / SUM(b.AtBats), 3) AS SluggingPercent
FROM workspace.baseball.silver_batting b
INNER JOIN workspace.baseball.silver_games g ON b.GameID = g.GameID AND g.GameType = ('regular')
INNER JOIN workspace.baseball.silver_teams t ON t.TeamID = b.TeamID
INNER JOIN workspace.baseball.silver_teamLeagues tl ON tl.TeamID = b.TeamID AND tl.FirstSeason <= g.Season AND (tl.LastSeason >= g.Season OR tl.LastSeason IS NULL)
INNER JOIN workspace.baseball.silver_Leagues l ON l.LeagueID = tl.LeagueID AND l.IsNegroLeague = False
GROUP BY g.Season
HAVING(SUM(b.AtBats)) > 0

UNION ALL

SELECT 
    g.Season,
    l.Name AS League,
    SUM(b.Hits - b.Doubles - b.Triples - b.HomeRuns) AS Singles,
    SUM(b.Doubles) AS Doubles,
    SUM(b.Triples) AS Triples,
    SUM(b.HomeRuns) AS Homeruns,
    SUM(b.AtBats) AS AtBats,
    ROUND(((SUM(b.Hits) - SUM(b.Doubles) - SUM(b.Triples) - SUM(b.HomeRuns)) + (SUM(b.Doubles) * 2) + (SUM(b.Triples) * 3) + (SUM(b.HomeRuns) * 4)) / SUM(b.AtBats), 3) AS SluggingPercent
FROM workspace.baseball.silver_batting b
INNER JOIN workspace.baseball.silver_games g ON b.GameID = g.GameID AND g.GameType = ('regular')
INNER JOIN workspace.baseball.silver_teams t ON t.TeamID = b.TeamID
INNER JOIN workspace.baseball.silver_teamLeagues tl ON tl.TeamID = b.TeamID AND tl.FirstSeason <= g.Season AND (tl.LastSeason >= g.Season OR tl.LastSeason IS NULL)
INNER JOIN workspace.baseball.silver_Leagues l ON l.LeagueID = tl.LeagueID AND l.IsNegroLeague = False
GROUP BY g.Season, l.Name
HAVING(SUM(b.AtBats)) > 0
ORDER BY g.Season DESC, League;
