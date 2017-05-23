for name in $(cat order.tsv); do
    echo "DYNASTY: $name"
    for injection in '乎' '耶' '兮' '哉' '夫' '矣' '也'; do
        echo $name $injection \
            $(find $name/poems/ -name "*.tsv" | xargs -I {} cat "{}" | cut -f 2 | grep $injection | wc -l)
    done
done