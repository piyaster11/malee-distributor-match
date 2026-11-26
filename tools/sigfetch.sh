cd data/sig
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36'
for c in china united-states united-arab-emirates saudi-arabia philippines malaysia australia united-kingdom; do for p in beverages processed-fruit-products; do
 curl -sL -m 20 -A "$UA" -o g4_${c}_${p}.html -w "%{http_code} g4 $c $p %{size_download}\n" "https://www.go4worldbusiness.com/buyers/$c/$p" & done; done; wait
for c in china usa uae saudi-arabia philippines malaysia australia uk; do for k in juice coconut-water; do
 curl -sL -m 20 -A "$UA" -o tk_${c}_${k}.html -w "%{http_code} tk $c $k %{size_download}\n" "https://importer.tradekey.com/$c/$k.htm" & done; done; wait
echo DONE
