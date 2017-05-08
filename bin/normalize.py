#!/bin/env python

import sys

import hgvs.parser
import hgvs.validator
import hgvs.normalizer
import hgvs.dataproviders.uta

from   hgvs.exceptions import HGVSError, HGVSParseError, HGVSInvalidVariantError, HGVSDataNotAvailableError, HGVSUnsupportedOperationError


hp  = hgvs.parser.Parser()

hdp = hgvs.dataproviders.uta.connect()

vr  = hgvs.validator.Validator(hdp, strict=False)

norm3c = hgvs.normalizer.Normalizer(hdp, shuffle_direction=3, cross_boundaries=True)
norm5c = hgvs.normalizer.Normalizer(hdp, shuffle_direction=5, cross_boundaries=True)
norm3  = hgvs.normalizer.Normalizer(hdp, shuffle_direction=3, cross_boundaries=False)
norm5  = hgvs.normalizer.Normalizer(hdp, shuffle_direction=5, cross_boundaries=False)


with open(sys.argv[1], 'r') as f:
    for var in f:
        var = var.rstrip('\n')

        try:
            var_i = hp.parse_hgvs_variant(var)
        except HGVSParseError as msg:
            print("ErrorParse\t{0}\t{1}".format(var, msg))
            continue

        try:
            vr.validate(var_i)
        except HGVSInvalidVariantError as msg:
            print("ErrorValidation\t{0}\t{1}".format(var, msg))
            continue
        except HGVSDataNotAvailableError as msg:
            print("ErrorNoData\t{0}\t{1}".format(var, msg))
            continue
        except HGVSError as msg:
            print("ErrorHGVS\t{0}\t{1}".format(var, msg))
            continue
        except Exception as msg:
            print("Error\t{0}\t{1}".format(var, msg))
            continue


        try:
            if var_i.type in 'gm':
                var_len = var_i.posedit.pos.end.base - var_i.posedit.pos.start.base + 1
                if var_len > 1000000:
                    raise Exception('Variant length is greater than 1M and would not be normalized')

            try:
                var_3c = norm3c.normalize(var_i)
            except HGVSUnsupportedOperationError:
                var_3c = 'Unsupported'
            try:
                var_5c = norm5c.normalize(var_i)
            except HGVSUnsupportedOperationError:
                var_5c = 'Unsupported'

            if var_i.type == 'c':
                try:
                    var_3 = norm3.normalize(var_i)
                except HGVSUnsupportedOperationError:
                    var_3 = 'Unsupported'
                try:
                    var_5 = norm5.normalize(var_i)
                except HGVSUnsupportedOperationError:
                    var_5 = 'Unsupported'
            else:
                var_3 = var_3c
                var_5 = var_5c

            print("{origin}\t{parsed}\t{var_3c}\t{var_5c}\t{var_3}\t{var_5}".format(
                   origin=var, parsed=var_i, var_3c=var_3c, var_5c=var_5c, var_3=var_3, var_5=var_5))
        except HGVSDataNotAvailableError as msg:
            print("ErrorNoData\t{0}\t{1}".format(var, msg))
            continue
        except HGVSError as msg:
            print("ErrorHGVS\t{0}\t{1}".format(var, msg))
            continue
        except Exception as msg:
            print("Error\t{0}\t{1}".format(var, msg))
            continue



