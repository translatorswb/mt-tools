MDIR="$HOME/extSW/mosesdecoder/scripts/generic"
  
REF_PATH=$1
HYP_PATH=$2

perl $MDIR/multi-bleu.perl -lc $REF_PATH < $HYP_PATH