#!/bin/env python

import sys
import sqlite3
from lxml import etree


with sqlite3.connect(sys.argv[2], isolation_level=None) as conn:
    with open(sys.argv[1], 'rb') as xml:
        for _, element in etree.iterparse(xml, tag='ClinVarSet'):
            status = element.find('RecordStatus').text
            if status != 'current':
                element.clear()
                continue
    
            record = element.find('ReferenceClinVarAssertion')
    
            acc_id = record.find('ClinVarAccession').get('Acc')
            assert_type = record.find('Assertion').get('Type')
    
            citation = record.find(".//ObservedIn/ObservedData/Citation")
            if citation is not None:
                pubmed_id   = citation.findtext('ID')
                description = citation.getparent().findtext(".//Attribute[@Type='Description']")
            else:
                pubmed_id   = None
                description = None
    
            disease = record.findtext(".//TraitSet/Trait/Name/ElementValue[@Type='Preferred']")
    
            var_c = record.findtext(".//MeasureSet/Measure/AttributeSet/Attribute[@Type='HGVS, coding, RefSeq']")
            if var_c is None:
                var_c = record.findtext(".//MeasureSet/Measure/AttributeSet/Attribute[@Type='HGVS, coding, LRG']")
                if var_c is None:
                    var_c = record.findtext(".//MeasureSet/Measure/AttributeSet/Attribute[@Type='HGVS, coding']")
    
            var_g = record.findtext(".//MeasureSet/Measure/AttributeSet/Attribute[@Type='HGVS, genomic, top level']")
            if var_g is None:
                var_g = record.findtext(".//MeasureSet/Measure/AttributeSet/Attribute[@Type='HGVS, genomic, RefSeqGene']")
                if var_g is None:
                    var_g = record.findtext(".//MeasureSet/Measure/AttributeSet/Attribute[@Type='HGVS, genomic, LRG']")
                    if var_g is None:
                        var_g = record.findtext(".//MeasureSet/Measure/AttributeSet/Attribute[@Type='HGVS, genomic, top level, previous']")
                        if var_g is None:
                            var_g = record.findtext(".//MeasureSet/Measure/AttributeSet/Attribute[@Type='HGVS, genomic, top level, other']")
                            if var_g is None:
                                var_g = record.findtext(".//MeasureSet/Measure/AttributeSet/Attribute[@Type='HGVS, genomic']")
    
            if var_c is None or var_g is None:
                var = record.findtext(".//MeasureSet/Measure/AttributeSet/Attribute[@Type='HGVS']")
                if var is not None:
                    if var_c is None and (var.find(':c.') != -1 or var.find(':n.') != -1 or var.find(':r.') != -1):
                        var_c = var
                    if var_g is None and (var.find(':g.') != -1 or var.find(':m.') != -1):
                        var_g = var

            try:
                conn.execute('INSERT INTO clinvar VALUES (?, ?, ?, ?, ?, ?, ?)', (acc_id, var_c, var_g, pubmed_id, assert_type, disease, description))
            except sqlite3.IntegrityError:
                sys.stderr.write('\t'.join((acc_id, str(var_c), str(var_g)))+'\n')

            element.clear()




