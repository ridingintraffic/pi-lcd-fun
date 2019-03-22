# Run PADD
# If we're on the PiTFT screen (ssh is xterm)
if [ "$TERM" == "linux" ] ; then
  while :
  do
    ./pi-tft.py
  done
fi
