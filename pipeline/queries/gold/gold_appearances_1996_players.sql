WITH Appearances AS (
    SELECT DISTINCT GameID, PlayerID
    FROM workspace.baseball.silver_fielding

    UNION 

    SELECT DISTINCT GameID, PlayerID
    FROM workspace.baseball.silver_batting

    UNION 

    SELECT DISTINCT GameID, PlayerID
    FROM workspace.baseball.silver_pitching
)

SELECT 
    a.PlayerID,
    g.Season,
    CONCAT(bio.LastName, ', ', bio.FirstName) AS Player,
    IF(bio.BirthCountry = 'USA', bio.BirthState, bio.BirthCountry) AS BirthPlace,
    COUNT(*) AS Appearances
FROM workspace.baseball.silver_games g
INNER JOIN appearances a ON g.GameID = a.GameID
INNER JOIN workspace.baseball.silver_biofile bio ON bio.PlayerID = a.PlayerID
WHERE 1=1
    AND bio.BirthYear = 1996
    AND g.GameType = 'regular'
GROUP BY ALL
ORDER BY a.PlayerID, g.season DESC;