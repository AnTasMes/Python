create database testing_json_paris
go
use testing_json_paris
go

create table states(
    id int IDENTITY(1,1),
    state varchar(20),
)

alter table states alter column state varchar(60)

insert into states(state) VALUES
('NEW'), ('QUEUED_FOR_PROCESSING'), ('PRE_PROCESSING'), ('FILE_TO_TIFF_CONVERSION_PROCESSING'),
('FILE_TO_TIFF_CONVERSION_FINISHED'), ('OCR_PROCESSING'), ('OCR_FINISHED')

SELECT s.PRE_STATE, s.POST_STATE
FROM
    (
        SELECT 
            STATE AS 'PRE_STATE',
            LEAD(STATE) OVER(ORDER BY id) AS 'POST_STATE'
        FROM STATES
    ) as s
WHERE s.POST_STATE IS NOT NULL


create database json_tst
go 
use json_tst
go

DECLARE @JSON_VAL NVARCHAR(MAX) =  
'
[ {
    "id" : "30b1491e-057a-45f8-974a-6b9c7e795860",
    "utcTimeStamp" : 1608620031101,
    "state" : "NEW"
  }, {
    "id" : "30b1491e-057a-45f8-974a-6b9c7e795860",
    "utcTimeStamp" : 1608620517242,
    "state" : "QUEUED_FOR_PROCESSING"
  }, {
    "id" : "30b1491e-057a-45f8-974a-6b9c7e795860",
    "utcTimeStamp" : 1608620517242,
    "state" : "PRE_PROCESSING"
  }, {
    "id" : "30b1491e-057a-45f8-974a-6b9c7e795860",
    "utcTimeStamp" : 1608620517242,
    "state" : "FILE_TO_TIFF_CONVERSION_PROCESSING"
  }, {
    "id" : "30b1491e-057a-45f8-974a-6b9c7e795860",
    "utcTimeStamp" : 1608620519905,
    "state" : "FILE_TO_TIFF_CONVERSION_FINISHED"
  }, {
    "id" : "30b1491e-057a-45f8-974a-6b9c7e795860",
    "utcTimeStamp" : 1608620519906,
    "state" : "OCR_PROCESSING"
  }, {
    "id" : "30b1491e-057a-45f8-974a-6b9c7e795860",
    "utcTimeStamp" : 1608620531379,
    "state" : "OCR_FINISHED"
  }, {
    "id" : "30b1491e-057a-45f8-974a-6b9c7e795860",
    "utcTimeStamp" : 1608620531379,
    "state" : "PRE_PROCESSING_FINISHED"
  }, {
    "id" : "30b1491e-057a-45f8-974a-6b9c7e795860",
    "utcTimeStamp" : 1608620531379,
    "state" : "PIPELINE_PROCESSING"
  }, {
    "id" : "30b1491e-057a-45f8-974a-6b9c7e795860",
    "utcTimeStamp" : 1608620593927,
    "state" : "PIPELINE_FINISHED"
  }, {
    "id" : "30b1491e-057a-45f8-974a-6b9c7e795860",
    "utcTimeStamp" : 1608620593927,
    "state" : "POST_PROCESSING"
  }, {
    "id" : "30b1491e-057a-45f8-974a-6b9c7e795860",
    "utcTimeStamp" : 1608620597438,
    "state" : "DOCUMENT_PROCESSED"
  } ,{
    "id" : "83e90160-a2b5-48a8-87da-4ed964e99c4f",
    "utcTimeStamp" : 1608619981852,
    "state" : "NEW"
  }, {
    "id" : "83e90160-a2b5-48a8-87da-4ed964e99c4f",
    "utcTimeStamp" : 1608620042585,
    "state" : "QUEUED_FOR_PROCESSING"
  }, {
    "id" : "83e90160-a2b5-48a8-87da-4ed964e99c4f",
    "utcTimeStamp" : 1608620042585,
    "state" : "PRE_PROCESSING"
  }, {
    "id" : "83e90160-a2b5-48a8-87da-4ed964e99c4f",
    "utcTimeStamp" : 1608620042586,
    "state" : "FILE_TO_TIFF_CONVERSION_PROCESSING"
  }, {
    "id" : "83e90160-a2b5-48a8-87da-4ed964e99c4f",
    "utcTimeStamp" : 1608620045579,
    "state" : "FILE_TO_TIFF_CONVERSION_FINISHED"
  }, {
    "id" : "83e90160-a2b5-48a8-87da-4ed964e99c4f",
    "utcTimeStamp" : 1608620045580,
    "state" : "OCR_PROCESSING"
  }, {
    "id" : "83e90160-a2b5-48a8-87da-4ed964e99c4f",
    "utcTimeStamp" : 1608620057083,
    "state" : "OCR_FINISHED"
  }, {
    "id" : "83e90160-a2b5-48a8-87da-4ed964e99c4f",
    "utcTimeStamp" : 1608620057083,
    "state" : "PRE_PROCESSING_FINISHED"
  }, {
    "id" : "83e90160-a2b5-48a8-87da-4ed964e99c4f",
    "utcTimeStamp" : 1608620057084,
    "state" : "PIPELINE_PROCESSING"
  }, {
    "id" : "83e90160-a2b5-48a8-87da-4ed964e99c4f",
    "utcTimeStamp" : 1608620112939,
    "state" : "PIPELINE_FINISHED"
  }, {
    "id" : "83e90160-a2b5-48a8-87da-4ed964e99c4f",
    "utcTimeStamp" : 1608620112939,
    "state" : "POST_PROCESSING"
  }, {
    "id" : "83e90160-a2b5-48a8-87da-4ed964e99c4f",
    "utcTimeStamp" : 1608620115283,
    "state" : "DOCUMENT_PROCESSED"
  }]
  '



SELECT
    id,
    utcTimeStamp,
    state
INTO #JSN
FROM openJSON(@JSON_VAL)
WITH(
    id Binary(64) '$.id',
    utcTimeStamp DECIMAL '$.utcTimeStamp',
    state VARCHAR(50) '$.state'
)

SELECT DISTINCT
  M.ID,
  'PRE_PROCESSING' as START_STATE,
  'PIPELINE_FINISHED' as END_STATE,
  ((
    SELECT 
    UTCTIMESTAMP
    FROM #JSN I
    WHERE I.ID = M.ID AND I.STATE = 'PIPELINE_FINISHED'
  ) -
  (
    SELECT 
    UTCTIMESTAMP
    FROM #JSN I
    WHERE I.ID = M.ID AND I.STATE = 'PRE_PROCESSING'
  )) AS DURATION 
FROM #JSN M;