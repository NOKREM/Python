# Numerology
# SÜRÜM:  v1.0
# YAZAN:  Mert Eren KONAN
# LİSANS: GPL v3
# TARİH:  28/06/2019 14:13

import sys

def numerolog (string):
    one_sum  = 0
    two_sum  = 0
    main_sum = 0
    # HARFLERİ TANIMLAMA
    alfabeno = [1,2,3,4,5,6,7,8,9,10,
                11,12,13,14,15,16,17,18,19,
                20,21,22,23,24,25,26,27,28,29]
    alfabe =   ["a", "b", "c", "ç", "d", "e", "f", "g", "ğ",
                "h", "ı", "i", "j", "k", "l", "m", "n", "o", "ö",
                "p", "r", "s", "ş", "t", "u", "ü", "v", "y", "z"]
    # BÜYÜK HARFE ÇEVİRME
    buyuk_alfabe = list(''.join(alfabe).upper())
    buyuk_alfabe[11]="İ" # İ Karakteri
    array_string = list(''.join(string))
    # Harfin Rakam Karşılığını Bulma
    for a in range(len(array_string)):
        for b in range(len(alfabe)):
            if array_string[a] == buyuk_alfabe[b] or array_string[a] == alfabe[b]:
               main_sum += alfabeno[b]
    one_sum = main_sum
    # Sonuç Çift Rakamlıysa Tek Rakama İndirgeme
    while len(list(str(one_sum))) > 1:
        arr_sum = list(str(one_sum))
        one_sum = 0
        for c in range(len(arr_sum)):
            one_sum += int(arr_sum[c])
        if len(list(str(one_sum))) == 2:
            two_sum = one_sum
    return one_sum,two_sum,main_sum;

numbers=numerolog(sys.argv[1:])
print(list(numbers))
print("Girdiğniz Kelime=%s\nAna Toplam=%s\nİki Rakamlı Sonuç=%s\nTek Rakamlı Sonuç=%s" % (' '.join(sys.argv[1:]),numbers[2],numbers[1],numbers[0]))
