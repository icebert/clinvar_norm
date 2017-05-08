#!/bin/env python

import sys
import sqlite3
import hgvs.parser

input = sys.argv[1]
vtype = sys.argv[2]
db    = sys.argv[3]

hp = hgvs.parser.Parser()


with sqlite3.connect(db, isolation_level=None) as conn:
    with open(input, 'r') as f:
        for line in f:
            (var, var_i, var_3c, var_5c, var_3, var_5) = line.rstrip('\n').split('\t')

            if var_3 != var_i and var_3 != 'Unsupported':
                hgvs_var_3 = hp.parse_hgvs_variant(var_3)
                hgvs_var_i = hp.parse_hgvs_variant(var_i)
                if hgvs_var_3.posedit.edit.type != hgvs_var_i.posedit.edit.type: # rewritten
                    conn.execute('INSERT INTO rewritable VALUES (?, ?, ?, ?, ?, ?)', (var, vtype, 3, 0, var_i, var_3))
                if str(hgvs_var_3.posedit.pos) != str(hgvs_var_i.posedit.pos): # probably shuffled
                    shuffled = True
                    if ( hgvs_var_i.posedit.edit.type == 'ins' and hgvs_var_3.posedit.edit.type == 'dup' and 
                         str(hgvs_var_3.posedit.pos.end) == str(hgvs_var_i.posedit.pos.start) ):
                        shuffled = False
                    if ( hgvs_var_i.posedit.edit.type == 'delins' and hgvs_var_3.posedit.edit.type == 'sub' and
                         str(hgvs_var_3.posedit.pos.start) == str(hgvs_var_i.posedit.pos.end) ):
                        shuffled = False
                    if ( hgvs_var_i.posedit.edit.type == 'delins' and hgvs_var_3.posedit.edit.type == 'del' and
                         str(hgvs_var_3.posedit.pos.start) == str(hgvs_var_i.posedit.pos.end) ):
                        shuffled = False
                    if shuffled:
                        conn.execute('INSERT INTO shiftable VALUES (?, ?, ?, ?, ?, ?)', (var, vtype, 3, 0, var_i, var_3))

            if var_5 != var_i and var_5 != 'Unsupported':
                hgvs_var_5 = hp.parse_hgvs_variant(var_5)
                hgvs_var_i = hp.parse_hgvs_variant(var_i)
                if hgvs_var_5.posedit.edit.type != hgvs_var_i.posedit.edit.type: # rewritten
                    conn.execute('INSERT INTO rewritable VALUES (?, ?, ?, ?, ?, ?)', (var, vtype, 5, 0, var_i, var_5))
                if str(hgvs_var_5.posedit.pos) != str(hgvs_var_i.posedit.pos): # probably shuffled
                    shuffled = True
                    if ( hgvs_var_i.posedit.edit.type == 'ins' and hgvs_var_5.posedit.edit.type == 'dup' and 
                         str(hgvs_var_5.posedit.pos.start) == str(hgvs_var_i.posedit.pos.end) ):
                        shuffled = False
                    if ( hgvs_var_i.posedit.edit.type == 'delins' and hgvs_var_5.posedit.edit.type == 'sub' and
                         str(hgvs_var_5.posedit.pos.start) == str(hgvs_var_i.posedit.pos.end) ):
                        shuffled = False
                    if ( hgvs_var_i.posedit.edit.type == 'delins' and hgvs_var_5.posedit.edit.type == 'del' and
                         str(hgvs_var_5.posedit.pos.start) == str(hgvs_var_i.posedit.pos.end) ):
                        shuffled = False
                    if shuffled:
                        conn.execute('INSERT INTO shiftable VALUES (?, ?, ?, ?, ?, ?)', (var, vtype, 5, 0, var_i, var_5))

            if var_3c != var_i and var_3c != 'Unsupported':
                hgvs_var_3c = hp.parse_hgvs_variant(var_3c)
                hgvs_var_i  = hp.parse_hgvs_variant(var_i)
                if hgvs_var_3c.posedit.edit.type != hgvs_var_i.posedit.edit.type: # rewritten
                    conn.execute('INSERT INTO rewritable VALUES (?, ?, ?, ?, ?, ?)', (var, vtype, 3, 1, var_i, var_3c))
                if str(hgvs_var_3c.posedit.pos) != str(hgvs_var_i.posedit.pos): # probably shuffled
                    shuffled = True
                    if ( hgvs_var_i.posedit.edit.type == 'ins' and hgvs_var_3c.posedit.edit.type == 'dup' and 
                         str(hgvs_var_3c.posedit.pos.end) == str(hgvs_var_i.posedit.pos.start) ):
                        shuffled = False
                    if ( hgvs_var_i.posedit.edit.type == 'delins' and hgvs_var_3c.posedit.edit.type == 'sub' and
                         str(hgvs_var_3c.posedit.pos.start) == str(hgvs_var_i.posedit.pos.end) ):
                        shuffled = False
                    if ( hgvs_var_i.posedit.edit.type == 'delins' and hgvs_var_3c.posedit.edit.type == 'del' and
                         str(hgvs_var_3c.posedit.pos.start) == str(hgvs_var_i.posedit.pos.end) ):
                        shuffled = False
                    if shuffled:
                        conn.execute('INSERT INTO shiftable VALUES (?, ?, ?, ?, ?, ?)', (var, vtype, 3, 1, var_i, var_3c))

            if var_5c != var_i and var_5c != 'Unsupported':
                hgvs_var_5c = hp.parse_hgvs_variant(var_5c)
                hgvs_var_i  = hp.parse_hgvs_variant(var_i)
                if hgvs_var_5c.posedit.edit.type != hgvs_var_i.posedit.edit.type: # rewritten
                    conn.execute('INSERT INTO rewritable VALUES (?, ?, ?, ?, ?, ?)', (var, vtype, 5, 1, var_i, var_5c))
                if str(hgvs_var_5c.posedit.pos) != str(hgvs_var_i.posedit.pos): # probably shuffled
                    shuffled = True
                    if ( hgvs_var_i.posedit.edit.type == 'ins' and hgvs_var_5c.posedit.edit.type == 'dup' and 
                         str(hgvs_var_5c.posedit.pos.start) == str(hgvs_var_i.posedit.pos.end) ):
                        shuffled = False
                    if ( hgvs_var_i.posedit.edit.type == 'delins' and hgvs_var_5c.posedit.edit.type == 'sub' and
                         str(hgvs_var_5c.posedit.pos.start) == str(hgvs_var_i.posedit.pos.end) ):
                        shuffled = False
                    if ( hgvs_var_i.posedit.edit.type == 'delins' and hgvs_var_5c.posedit.edit.type == 'del' and
                         str(hgvs_var_5c.posedit.pos.start) == str(hgvs_var_i.posedit.pos.end) ):
                        shuffled = False
                    if shuffled:
                        conn.execute('INSERT INTO shiftable VALUES (?, ?, ?, ?, ?, ?)', (var, vtype, 5, 1, var_i, var_5c))




