SELECT 
    CAST(ParkID AS STRING) AS ParkID,
    CAST(Name AS STRING) AS Name,
    CAST(AKA AS STRING) AS AltName,
    CAST(City AS STRING) AS City,
    CAST(State AS STRING) AS State,
    TO_DATE(START, 'M/d/yyyy') AS StartDate,
    TO_DATE(END, 'M/d/yyyy') AS EndDate,
    CAST(League AS STRING) AS League,
    CAST(Notes AS STRING) AS Notes
FROM workspace.baseball.bronze_ballparks;