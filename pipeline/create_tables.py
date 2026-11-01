import os

# Load data into spark
def create_bronze_tables(target_dir: str) -> None:
    for file in os.listdir(target_dir):
        try:
            file_name = str(file.split('.')[0])
            df = spark.read.csv(os.path.join(target_dir, file), header=True, inferSchema=False)        
            df.write.format('delta').mode('overwrite').saveAsTable(f'workspace.baseball.bronze_{file_name}')
            print(f'Successfully loaded file {file}')
        except Exception as e:
            print(f'Error loading file {file}. Exception {e}')

def create_silver_tables() -> None:
    ballparks_df = spark.sql('''
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
        FROM workspace.baseball.bronze_ballparks
    ''')

    batting_df = spark.sql('''
        SELECT 
            CAST(gid AS STRING) AS GameID,
            CAST(id AS STRING) AS PlayerID,
            CAST(team AS STRING) AS TeamID,
            CAST(b_lp AS INT) AS PositionID,
            CAST(b_seq AS INT) AS Sequence,
            CAST(b_pa AS INT) as PlateAppearances,
            CAST(b_ab AS INT) AS AtBats,
            CAST(b_r AS INT) AS Runs,
            CAST(b_h AS INT) AS Hits,
            CAST(b_d AS INT) AS Doubles,
            CAST(b_t AS INT) AS Triples,
            CAST(b_hr AS INT) AS HomeRuns,
            CAST(b_rbi AS INT) AS RBIs,
            CAST(b_sh AS INT) AS SacrificeHits,
            CAST(b_sf AS INT) AS SacrificeFlies,
            CAST(b_hbp AS INT) AS HitByPitch,
            CAST(b_w AS INT) AS Walks,
            CAST(b_iw AS INT) AS IntentionalWalks,
            CAST(b_k AS INT) AS Strikeouts,
            CAST(b_sb AS INT) AS StolenBases,
            CAST(b_cs AS INT) AS CaughtStealing,
            CAST(b_gdp AS INT) AS GroundedIntoDoublePlays,
            CAST(b_xi AS INT) AS CatcherInterference,
            CAST(b_roe AS INT) AS ReachedByError,
            IF(dh IS NULL OR dh = 0, false, true) AS DesignatedHitter,
            IF(ph IS NULL OR ph = 0, false, true) AS PinchHit,
            IF(pr IS NULL OR pr = 0, false, true) AS PinchRun
        FROM workspace.baseball.bronze_batting
    ''')

    biofile_df = spark.sql('''
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
        FROM workspace.baseball.bronze_biofile
    ''')

    currentnames_df = spark.sql('''
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
        FROM workspace.baseball.bronze_currentnames
    ''')

    fielding_df = spark.sql('''
        SELECT 
            CAST(gid AS STRING) AS GameID,
            CAST(id AS STRING) AS PlayerID,
            CAST(team AS STRING) AS TeamID,
            CAST(d_seq AS INT) AS Sequence,
            CAST(d_pos AS INT) AS PositionID,
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
        FROM workspace.baseball.bronze_fielding
        WHERE id = 'mauej001'
    ''')

    game_df = spark.sql('''
        SELECT 
            CAST(gid AS STRING) AS GameID,
            CAST(visteam AS STRING) AS VisitingTeamID,
            CAST(hometeam AS STRING) AS HomeTeamID,
            CAST(site AS STRING) AS BallparkID,
            TO_DATE(date, 'yyyyMMdd') AS Date,
            CAST(number AS INT) AS GameNumber,
            IF(starttime IS NULL or starttime = '0:00PM', NULL, CAST(TO_TIMESTAMP(starttime, 'h:mma') AS TIME)) AS StartTime,
            CAST(daynight AS STRING) AS DayNight,
            IF(innings IS NULL, 9, CAST(innings AS INT)) AS ScheduledInnings,
            IF(tiebreaker IS NULL OR tiebreaker = '', false, true) AS TiebreakerUsed,
            IF(usedh IS NULL OR usedh = 'FALSE', false, true) AS DesignatedHitterUsed,
            IF(htbf IS NULL OR htbf = 'FALSE', false, true) AS HomeTeamBattedFirst,
            IF(timeofgame IS NULL OR timeofgame = 0, NULL, CAST(timeofgame AS INT)) AS TimeOfGameMinutes,
            CAST(attendance AS INT) AS Attendance,
            CAST(fieldcond AS STRING) AS FieldCondition,
            CAST(precip AS STRING) AS Precipitation,
            CAST(sky AS STRING) AS SkyCondition,
            IF(temp = 0, NULL, CAST(temp AS INT)) AS Temperature,
            CAST(winddir AS STRING) AS WindDirection,
            IF(windspeed = '-1', NULL, CAST(windspeed AS INT)) AS WindSpeed,
            IF(forfeit IS NULL OR forfeit = '', false, true) AS Forfeited,
            CAST(suspend AS STRING) AS SuspendedReplayDate,
            CAST(wp AS STRING) AS WinningPitcherID,
            CAST(lp AS STRING) AS LosingPitcherID,
            CAST(save AS STRING) AS SavePitcherID,
            CAST(gametype AS STRING) AS GameType,
            CAST(vruns AS INT) AS VisitingTeamRuns,
            CAST(hruns AS INT) AS HomeTeamRuns,
            CAST(wteam AS STRING) AS WinningTeamID,
            CAST(lteam AS STRING) AS LosingTeamID,
            CAST(season AS INT) AS Season
        FROM workspace.baseball.bronze_gameinfo
    ''')

    pitching_df = spark.sql('''
        SELECT 
            CAST(gid AS STRING) AS GameID,
            CAST(id AS STRING) AS PlayerID,
            CAST(team AS STRING) AS TeamID,
            CAST(p_seq AS INT) AS PitcherSequence,
            CAST(p_ipouts AS INT) AS OutsRecorded,
            CAST(p_noout AS INT) AS BattersFacedNoOutsRecorded,
            CAST(p_bfp AS INT) AS BattersFaced,
            CAST(p_h AS INT) AS HitsAllowed,
            CAST(p_d AS INT) AS DoublesAllowed,
            CAST(p_t AS INT) AS TriplesAllowed,
            CAST(p_hr AS INT) AS HomeRunsAllowed,
            CAST(p_r AS INT) AS RunsAllowed,
            CAST(p_er AS INT) AS EarnedRuns,
            CAST(p_w AS INT) AS WalksAllowed,
            CAST(p_iw AS INT) AS IntentionalWalks,
            CAST(p_k AS INT) AS Strikeouts,
            CAST(p_hbp AS INT) AS HitByPitch,
            CAST(p_wp AS INT) AS WildPitches,
            CAST(p_bk AS INT) AS Balks,
            CAST(p_sh AS INT) AS SacrificeHitsAllowed,
            CAST(p_sf AS INT) AS SacrificeFliesAllowed,
            CAST(p_sb AS INT) AS StolenBasesAllowed,
            CAST(p_cs AS INT) AS CaughtStealingAllowed,
            CAST(p_pb AS INT) AS PassedBallsAllowed,
            IF(wp IS NULL OR wp = 0, false, true) AS WinningPitcher,
            IF(lp IS NULL OR lp = 0, false, true) AS LosingPitcher,
            IF(save IS NULL OR save = 0, false, true) AS Save,
            IF(p_gs IS NULL OR p_gs = 0, false, true) AS GameStarted,
            IF(p_gf IS NULL OR p_gf = 0, false, true) AS GameFinished,
            IF(p_cg IS NULL OR p_cg = 0, false, true) AS CompleteGame
        FROM workspace.baseball.bronze_pitching
    ''')

if __name__ == '__main__':
    create_bronze_tables('/Volumes/workspace/baseball/baseball_raw/')