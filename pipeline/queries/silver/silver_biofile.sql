SELECT 
    CAST(PLAYERID AS STRING) AS PlayerID,
    CAST(LAST AS STRING) AS LastName,
    CAST(FIRST AS STRING) AS FirstName,
    CAST(NICKNAME AS STRING) AS Nickname,
    CASE 
        WHEN LENGTH(BIRTHDATE) = 4 THEN CAST(BIRTHDATE AS INT)
        WHEN BIRTHDATE LIKE '%/%/%' THEN CAST(SPLIT(BIRTHDATE, '/')[2] AS INT)
        ELSE NULL
    END AS BirthYear,
    CASE 
        WHEN BIRTHDATE LIKE '%/%/%' THEN CAST(SPLIT(BIRTHDATE, '/')[0] AS INT)
        ELSE NULL
    END AS BirthMonth,
    CASE 
        WHEN BIRTHDATE LIKE '%/%/%' THEN CAST(SPLIT(BIRTHDATE, '/')[1] AS INT)
        ELSE NULL
    END AS BirthDay,
    CAST(`BIRTH.CITY` AS STRING) AS BirthCity,
    CAST(`BIRTH.STATE` AS STRING) AS BirthState,
    CAST(`BIRTH.COUNTRY` AS STRING) AS BirthCountry,
    TO_DATE(`PLAY.DEBUT`, 'MM/dd/yyyy') AS Debut,
    TO_DATE(`PLAY.LASTGAME`, 'MM/dd/yyyy') AS LastGame,
    TRY_TO_DATE(`DEATHDATE`, 'MM/dd/yyyy') AS DeathDate,
    CAST(`DEATH.CITY` AS STRING) AS DeathCity,
    CAST(`DEATH.STATE` AS STRING) AS DeathState,
    CAST(`DEATH.COUNTRY` AS STRING) AS DeathCountry,
    CAST(BATS AS STRING) AS Bats,
    CAST(THROWS AS STRING) AS Throws,
    CAST(SPLIT(HEIGHT, '-')[0] AS INT) AS HeightFeet,
    CAST(SPLIT(HEIGHT, '-')[1] AS FLOAT) AS HeightInches,
    CAST(`BIRTH.NAME` AS STRING) AS Birthname,
    IF(HOF = 'HOF', true, false) AS HallOfFame
FROM workspace.baseball.bronze_biofile;