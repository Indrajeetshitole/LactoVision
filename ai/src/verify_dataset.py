import pandas as pd
from .config import *
from .preprocessing import load_train_test

def main():
    train,test=load_train_test()
    assert TARGET not in FEATURES
    forbidden=set(LEAKAGE_COLUMNS+IDENTIFIER_COLUMNS)
    assert not forbidden.intersection(FEATURES), forbidden.intersection(FEATURES)
    assert len(train)==40000 and len(test)==10000
    print('DATASET VERIFICATION PASSED')
    print('Train:',train.shape,'Test:',test.shape)
    print('Features:',len(FEATURES))
    print('Target:',TARGET)
    print('Excluded leakage/reporting columns:',sorted(set(LEAKAGE_COLUMNS).intersection(train.columns)))
    print('Excluded identifiers:',IDENTIFIER_COLUMNS)
if __name__=='__main__': main()
