cd /tmp

echo "Starting process"
python ./steam_reviews.py
echo "got all steam reviews"
python ./file_organizer.py
echo "sorted all reviews"
python ./pushpydrive.py
echo "uploaded to google drive"
echo "process completed"