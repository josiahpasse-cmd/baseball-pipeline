SELECT
    CAST(TeamCode AS STRING) AS TeamID,
    CAST(LeagueCode AS STRING) AS LeagueID,
    CAST(FirstSeason AS INT) AS FirstSeason,
    CAST(LastSeason AS INT) As LastSeason
FROM workspace.baseball.bronze_teamleagues;