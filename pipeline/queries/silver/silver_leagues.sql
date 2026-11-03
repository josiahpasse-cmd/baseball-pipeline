SELECT
    CAST(LeagueCode AS STRING) AS LeagueID,
    CAST(LeagueName AS STRING) AS Name,
    CAST(IsNegroLeague AS BOOLEAN) AS IsNegroLeague
FROM workspace.baseball.bronze_leagues;