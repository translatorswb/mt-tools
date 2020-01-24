METEOR_PATH="/home/twbgmy/extSW/meteor-1.5"

REF_PATH=$1
HYP_PATH=$2

java -Xmx2G -jar $METEOR_PATH/meteor-1.5.jar $HYP_PATH $REF_PATH -l en -norm | grep "Final score"
