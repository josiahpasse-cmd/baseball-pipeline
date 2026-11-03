SELECT
    CAST(PositionID AS INT) AS PositionID,
    CAST(Name AS STRING) AS Name,
    CAST(Abbreviation AS STRING) AS Abbreviation,
    CAST(Category AS STRING) AS Category
FROM workspace.baseball.bronze_positions;