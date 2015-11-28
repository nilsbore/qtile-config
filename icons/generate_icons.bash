
for f in *.svg; do
    s=${f##*/};
    convert -background none -density 2000 -resize 22x22 $f ${s%.*}.png;
done

cp battery_empty.png battery-missing.png
cp battery_two_thirds.png battery-good.png
cp battery_plugged.png battery-full.png
cp battery_empty.png battery-caution-charging.png
cp battery_plugged.png battery-low-charging.png
cp battery_plugged.png battery-good-charging.png
cp battery_plugged.png battery-full-charging.png
cp battery_plugged.png battery-full-charged.png
