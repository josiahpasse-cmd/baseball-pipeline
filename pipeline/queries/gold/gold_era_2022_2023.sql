WITH 2223Stats AS (
    SELECT
        p.PlayerID,
        g.Season,
        ROUND((SUM(p.EarnedRuns) * 9) / (SUM(p.OutsRecorded)/3), 3) AS ERA
    FROM workspace.baseball.silver_pitching p
    INNER JOIN workspace.baseball.silver_games g ON g.GameID = p.GameID
    WHERE 1=1
        AND g.GameType IN ('regular')
        AND g.Season IN (2022, 2023)
    GROUP BY ALL
    HAVING SUM(p.OutsRecorded) >= 216
)

SELECT
    b.PlayerID,
    CONCAT(b.LastName, ', ', b.FirstName) AS Player,
    AVG(s1.ERA) AS 2022ERA,
    AVG(s2.ERA) AS 2023ERA
FROM workspace.baseball.silver_biofile b
INNER JOIN 2223Stats s1 ON s1.PlayerID = b.PlayerID AND s1.Season = '2022'
INNER JOIN 2223Stats s2 ON s2.PlayerID = b.PlayerID AND s2.Season = '2023'
GROUP BY ALL
ORDER BY b.PlayerID;