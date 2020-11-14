#!/bin/bash

PWD=`pwd`
PWD="$PWD/getLeaderboardLambda"
FILES="$PWD/getLeaderboard.zip $PWD/getLeaderboard.py"

rm "$PWD/getLeaderboard.zip"
zip -r9 $FILES
echo "File successfully zipped"

aws lambda update-function-code --function-name yeetcode2020-getLeaderboard --zip-file fileb://"$PWD/getLeaderboard.zip"

echo "Published to lambda"

exit 0