SELECT
    CAST(TEAM AS STRING) AS TeamID,
    CAST(NICKNAME AS STRING) AS Nickname,
    CAST(FIRST AS INT) AS FirstSeason,
    IF(LAST = (SELECT MAX(LAST) FROM workspace.baseball.bronze_teams), NULL, CAST(LAST AS INT)) AS LastSeason
FROM workspace.baseball.bronze_teams;