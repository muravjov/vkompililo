#!/usr/bin/env python
# coding: utf-8

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("download_data_fdir")
    parser.add_argument("dst_txtfile")
    
    dst_fname = parser.parse_args().dst_txtfile
    
    import parse_vip
    parse_vip.setup_download_data(parser.parse_args().download_data_fdir)
    parse_vip.create_vip_vortaro(dst_fname)
