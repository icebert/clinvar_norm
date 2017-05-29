#!/bin/env python

import sys
import sqlite3

input = sys.argv[1]
vtype = sys.argv[2]
db    = sys.argv[3]
outf  = sys.argv[4]

with sqlite3.connect(db, isolation_level=None) as conn:
    with open(outf, 'w') as out:
        with open(input, 'r') as f:
            for line in f:
                line = line.rstrip('\n')
                if line.startswith('Error'):
                    (error, var, reason) = line.split('\t')
                    if error == 'ErrorParse':
                        error = 'parse error'
                    elif error == 'ErrorNoData':
                        error = 'data not available'
                    elif error == 'ErrorHGVS':
                        error = 'coordinate out of bounds'
                    elif error == 'ErrorValidation':
                        if 'reference sequence' in reason:
                            error = 'wrong reference'
                        elif 'out of the bound' in reason:
                            error = 'coordinate out of bounds'
                        else:
                            error = 'discordant del/ins length'
                    else:
                        if 'length is greater than' in reason:
                            error = 'variant greater than 1M'
                        else:
                            error = 'namespace is none'
                    conn.execute('INSERT INTO error VALUES (?, ?, ?, ?)', (var, vtype, error, reason))
                else:
                    (var, var_i, var3c, var5c, var3, var5) = line.split('\t')
                    if var3c == 'Unsupported' and var5c == 'Unsupported' and var3 == 'Unsupported' and var5 == 'Unsupported': # intronic
                        conn.execute('INSERT INTO intronic VALUES (?)', (var, ))
                    else:
                        out.write(line+'\n')



