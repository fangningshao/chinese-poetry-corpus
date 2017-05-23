for name in $(cat order.tsv); do
    echo $name \
    $(find $name/poems/ -name "*.tsv" | xargs -I {} cat "{}" | cut -f 1 | grep 绝句 | wc -l) \
    $(find $name/poems/ -name "*.tsv" | xargs -I {} cat "{}" | cut -f 1 | grep 律诗 | wc -l)
done