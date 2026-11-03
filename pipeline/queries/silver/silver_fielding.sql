SELECT 
    CAST(gid AS STRING) AS GameID,
    CAST(id AS STRING) AS PlayerID,
    CAST(team AS STRING) AS TeamID,
    CAST(d_seq AS INT) AS Sequence,
    IF(d_pos = '?', NULL, CAST(d_pos AS INT)) AS PositionID,
    CAST(d_ifouts AS INT) AS OutsPlayed,
    CAST(d_po AS INT) AS Putouts,
    CAST(d_a AS INT) AS Assists,
    CAST(d_e AS INT) AS Errors,
    CAST(d_dp AS INT) AS DoublePlays,
    CAST(d_tp AS INT) AS TriplePlays,
    CAST(d_pb AS INT) AS PassedBalls,
    CAST(d_wp AS INT) AS WildPitches,
    CAST(d_sb AS INT) AS StolenBasesAllowed,
    CAST(d_cs AS INT) AS CaughtStealing,
    IF(d_gs IS NULL OR d_gs = 0, false, true) AS GameStartedAtPosition
FROM workspace.baseball.bronze_fielding;