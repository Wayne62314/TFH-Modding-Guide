"""Read a Reverge Package File 1.1 index only. Never extract or modify assets."""
import argparse,json,struct
from pathlib import Path

def read_index(stream,size):
    def take(n):
        if n<0 or stream.tell()+n>size:raise ValueError('Truncated index')
        data=stream.read(n)
        if len(data)!=n:raise ValueError('Short read')
        return data
    def u32():return struct.unpack('>I',take(4))[0]
    def u64():return struct.unpack('>Q',take(8))[0]
    def string():
        length=u64()
        if length>65536:raise ValueError('String safety limit')
        return take(length).decode('utf-8')
    start=u32()
    if start>size:raise ValueError('Data region outside file')
    if string()!='Reverge Package File' or string()!='1.1':raise ValueError('Unsupported package/version')
    count=u64()
    if count>1000000 or stream.tell()+count*20>start:raise ValueError('Invalid index count/bounds')
    offset=start;entries=[]
    for _ in range(count):
        name=string();length=u64();alignment=u32()
        if alignment==0:raise ValueError('Invalid alignment')
        offset+=(-offset)%alignment
        if offset+length>size:raise ValueError('Entry outside file')
        entries.append({'path':name,'offset':offset,'size':length,'alignment':alignment});offset+=length
    if stream.tell()>start:raise ValueError('Index overlaps data')
    return {'format':'Reverge Package File','version':'1.1','file_size':size,'data_offset':start,'entries':entries}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('package',type=Path);args=p.parse_args()
    with args.package.open('rb') as f:result=read_index(f,args.package.stat().st_size)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
