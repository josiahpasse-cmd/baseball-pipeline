SELECT 
    CAST(TEAMID AS STRING) AS TeamID,
    CAST(CURTEAMID AS STRING) AS CurrentTeamID,
    CAST(STATE AS STRING) AS State,
    CAST(DIV AS STRING) AS Division,
    CAST(CITY AS STRING) AS City,
    CAST(NAME AS STRING) AS Name,
    CAST(ALTNAME AS STRING) AS AltName,
    TO_DATE(START, 'M/d/yyyy') AS StartDate,
    TO_DATE(END, 'M/d/yyyy') AS EndDate,
    CAST(STADIUMCITY AS STRING) AS StadiumCity,
    CAST(STADIUMSTATE AS STRING) AS StadiumState
FROM workspace.baseball.bronze_currentnames;