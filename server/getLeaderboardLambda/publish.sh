#!/bin/bash

rm getLeaderboard.zip
zip -r9 getLeaderboard.zip *.py
echo "File successfully zipped"

aws lambda update-function-code --function-name yeetcode2020-getLeaderboard --zip-file fileb://getLeaderboard.zip

echo "Published to lambda"

exit 0
